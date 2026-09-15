from typing import Tuple, Dict, Any, List, Optional
from backend.app.compression.base import BaseCompressor
from backend.app.models.prompt import CompressionConfig
from backend.app.models.optimization import CompressionResult
from backend.app.services.protection_engine import ProtectionEngine
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)

class AdaptiveCompressor(BaseCompressor):
    """
    Optimized Adaptive Compressor for Phase 6.75.
    Reuses single protection mapping, strictly enforces MAX_MODEL_CALLS=4 cap,
    mathematically maintains safe lower/upper search bounds, tracks fallback reasons,
    and guarantees that fallbacks strictly return original prompt text.
    """
    
    def __init__(self, base_compressor: BaseCompressor, max_model_calls: int = settings.MAX_MODEL_CALLS):
        self.base_compressor = base_compressor
        self.protection_engine = ProtectionEngine()
        self.validator = ConstraintValidator()
        self.max_model_calls = max_model_calls
        
    @property
    def name(self) -> str:
        return f"Adaptive({self.base_compressor.name})"
        
    @property
    def is_available(self) -> bool:
        return self.base_compressor.is_available
        
    def compress(self, text: str, config: CompressionConfig) -> CompressionResult:
        return self.compress_with_telemetry(text, config)[0]

    def compress_with_telemetry(self, text: str, config: CompressionConfig) -> Tuple[CompressionResult, Dict[str, Any]]:
        telemetry = {
            "llmlingua_calls": 0,
            "iterations": 0,
            "validation_attempts": 0,
            "compression_attempts": 0,
            "retention_rates": [],
            "validation_results": [],
            "failure_reasons": [],
            "fallback_reason": "NONE"
        }
        
        if not text:
            res = CompressionResult(
                original_text=text,
                compressed_text=text,
                original_tokens=0,
                compressed_tokens=0,
                compression_ratio=1.0,
                saving_percent=0.0,
                mode_used=config.mode.value,
                status='safe'
            )
            return res, telemetry

        # Mask prompt ONCE before search loop
        masked_prompt, mapping = self.protection_engine.mask(text)

        min_rate_delta = 0.02
        min_retention_rate = 0.40
        max_retention_rate = 1.00
        
        best_valid_result = None
        last_failure_reason = "CONSTRAINT_VALIDATION_FAILURE"

        # Candidate retention rates search
        if config.target_rate is not None:
            initial_rates = [config.target_rate, 0.85, 0.925]
        else:
            initial_rates = [0.60, 0.80, 0.90]

        for iteration in range(self.max_model_calls):
            if (max_retention_rate - min_retention_rate) < min_rate_delta:
                logger.info(f"Interval delta below threshold {min_rate_delta} after {iteration} iterations.")
                break

            if iteration == 0 and config.target_rate is not None:
                current_rate = initial_rates[0]
            else:
                current_rate = (min_retention_rate + max_retention_rate) / 2.0

            telemetry["iterations"] += 1
            telemetry["retention_rates"].append(round(current_rate, 4))
            telemetry["llmlingua_calls"] += 1
            telemetry["compression_attempts"] += 1

            # Hard assertion: max_model_calls limit
            assert telemetry["llmlingua_calls"] <= self.max_model_calls, f"Model calls exceeded limit {self.max_model_calls}"

            rate_config = CompressionConfig(
                mode=config.mode,
                target_rate=current_rate,
                force_tokens=config.force_tokens,
                target_model=config.target_model
            )

            compressed_masked = self.base_compressor.compress(masked_prompt, rate_config)

            if compressed_masked.status == 'failed':
                telemetry["validation_results"].append("FAILED_COMPRESSION")
                telemetry["failure_reasons"].append("LLMLingua inference error")
                last_failure_reason = "NO_SAFE_COMPRESSION"
                min_retention_rate = current_rate
                continue

            restored_prompt = self.protection_engine.unmask(compressed_masked.compressed_text, mapping)

            # Placeholder integrity check
            if not self.protection_engine.validate_placeholders(compressed_masked.compressed_text, mapping):
                telemetry["validation_results"].append("FAILED_PLACEHOLDERS")
                telemetry["failure_reasons"].append("Placeholder corruption")
                last_failure_reason = "STRUCTURAL_VALIDATION_FAILURE"
                min_retention_rate = current_rate
                continue

            telemetry["validation_attempts"] += 1
            validation_res = self.validator.validate(text, restored_prompt)
            is_valid = validation_res.status == "PASS"

            if is_valid:
                telemetry["validation_results"].append("PASS")
                logger.info(f"Iteration {iteration}: rate {current_rate:.4f} PASSED.")
                result = CompressionResult(
                    original_text=text,
                    compressed_text=restored_prompt,
                    original_tokens=compressed_masked.original_tokens,
                    compressed_tokens=compressed_masked.compressed_tokens,
                    compression_ratio=compressed_masked.compression_ratio,
                    saving_percent=compressed_masked.saving_percent,
                    mode_used=config.mode.value,
                    status='safe'
                )
                best_valid_result = result
                max_retention_rate = current_rate
            else:
                reason = validation_res.critical_failures[0] if validation_res.critical_failures else "Constraint violation"
                telemetry["validation_results"].append("FAIL")
                telemetry["failure_reasons"].append(reason)
                last_failure_reason = "CONSTRAINT_VALIDATION_FAILURE"
                logger.info(f"Iteration {iteration}: rate {current_rate:.4f} FAILED ({reason}).")
                min_retention_rate = current_rate

        if best_valid_result is not None:
            telemetry["fallback_reason"] = "NONE"
            return best_valid_result, telemetry

        # Fallback strictly returns original prompt text
        logger.warning(f"No compressed rate passed validation. Falling back to original prompt ({last_failure_reason}).")
        orig_tokens = len(text.split())
        fallback_res = CompressionResult(
            original_text=text,
            compressed_text=text,
            original_tokens=orig_tokens,
            compressed_tokens=orig_tokens,
            compression_ratio=1.0,
            saving_percent=0.0,
            mode_used=config.mode.value,
            status='failed'
        )
        
        # Hard assertion: fallback must strictly match original text
        assert fallback_res.compressed_text == text, "Fallback compressed_text must strictly equal original_text"
        
        if telemetry["llmlingua_calls"] >= self.max_model_calls:
            telemetry["fallback_reason"] = "MAX_MODEL_CALLS_REACHED"
        else:
            telemetry["fallback_reason"] = last_failure_reason

        return fallback_res, telemetry
