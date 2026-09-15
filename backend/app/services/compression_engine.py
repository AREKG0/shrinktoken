import time
from typing import Optional, List, Tuple, Dict, Any
from backend.app.compression.base import BaseCompressor
from backend.app.compression.llmlingua import LLMLinguaCompressor
from backend.app.compression.adaptive import AdaptiveCompressor
from backend.app.compression.compressibility_analyzer import CompressibilityAnalyzer
from backend.app.services.rag_strategy import RAGStrategy
from backend.app.services.segment_compressor import SegmentCompressor
from backend.app.models.prompt import CompressionConfig, CompressionMode
from backend.app.models.optimization import CompressionResult
from backend.app.models.telemetry import OptimizationTelemetry
from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)

class CompressionService:
    def __init__(self, compressor: BaseCompressor, max_model_calls: int = settings.MAX_MODEL_CALLS):
        self.raw_compressor = compressor
        self.adaptive_compressor = AdaptiveCompressor(compressor, max_model_calls=max_model_calls)
        self.analyzer = CompressibilityAnalyzer(min_token_savings=settings.MINIMUM_TOKEN_SAVINGS, min_compressible_length=settings.MIN_COMPRESSIBLE_LENGTH)
        self.rag_strategy = RAGStrategy()
        self.segment_compressor = SegmentCompressor()
        
    def get_token_count(self, text: str) -> int:
        if hasattr(self.raw_compressor, "get_token_count"):
            return self.raw_compressor.get_token_count(text)
        return len(text.split())

    def optimize_with_telemetry(self, text: str, mode: CompressionMode, prompt_id: str = "", category: str = "general", target_rate: Optional[float] = None, force_tokens: Optional[List[str]] = None) -> Tuple[CompressionResult, OptimizationTelemetry]:
        t0 = time.time()
        orig_tokens = self.get_token_count(text)
        
        telemetry = OptimizationTelemetry(
            request_id=f"req-{prompt_id if prompt_id else 'direct'}",
            prompt_id=prompt_id,
            category=category,
            original_token_count=orig_tokens
        )
        
        p_t0 = time.time()
        # 1. Compressibility Analyzer Early Exit Filter
        analysis = self.analyzer.analyze(text, category=category)
        prot_time = round((time.time() - p_t0) * 1000.0, 2)
        telemetry.protection_time = prot_time
        telemetry.protection_time_ms = prot_time

        if not analysis["compressible"]:
            logger.info(f"Early exit triggered by CompressibilityAnalyzer ({analysis['reason']})")
            tot_time = round((time.time() - t0) * 1000.0, 2)
            telemetry.early_exit = True
            telemetry.early_exit_reason = analysis["reason"]
            telemetry.final_token_count = orig_tokens
            telemetry.tokens_saved = 0
            telemetry.compression_percentage = 0.0
            telemetry.total_time = tot_time
            telemetry.total_time_ms = tot_time
            
            res = CompressionResult(
                original_text=text,
                compressed_text=text,
                original_tokens=orig_tokens,
                compressed_tokens=orig_tokens,
                compression_ratio=1.0,
                saving_percent=0.0,
                mode_used=mode.value,
                status='safe'
            )
            return res, telemetry

        config = CompressionConfig(mode=mode, target_rate=target_rate, force_tokens=force_tokens)

        # 2. Category-Aware Strategy Routing
        c_t0 = time.time()
        
        if category == "rag":
            rag_res = self.rag_strategy.compress_rag(text, self.raw_compressor, self.get_token_count)
            comp_time = round((time.time() - c_t0) * 1000.0, 2)
            tot_time = round((time.time() - t0) * 1000.0, 2)
            
            telemetry.compression_time = comp_time
            telemetry.compression_time_ms = comp_time
            telemetry.number_of_llmlingua_calls = rag_res["model_calls"]
            telemetry.number_of_adaptive_iterations = rag_res["model_calls"]
            telemetry.compression_attempts = rag_res["model_calls"]
            telemetry.validation_attempts = rag_res["model_calls"]
            telemetry.fallback = rag_res["fallback"]
            telemetry.fallback_reason = "NONE" if not rag_res["fallback"] else "CONSTRAINT_VALIDATION_FAILURE"
            telemetry.final_token_count = rag_res["opt_total_tokens"]
            telemetry.tokens_saved = max(0, orig_tokens - rag_res["opt_total_tokens"])
            telemetry.compression_percentage = rag_res["total_reduction_percent"]
            telemetry.total_time = tot_time
            telemetry.total_time_ms = tot_time

            res = CompressionResult(
                original_text=text,
                compressed_text=rag_res["compressed_text"],
                original_tokens=orig_tokens,
                compressed_tokens=rag_res["opt_total_tokens"],
                compression_ratio=round(rag_res["opt_total_tokens"] / max(1, orig_tokens), 4),
                saving_percent=rag_res["total_reduction_percent"],
                mode_used=mode.value,
                status='safe' if not rag_res["fallback"] else 'failed'
            )
            return res, telemetry

        # 3. Multi-Constraint & General Adaptive Selective Compression
        opt_res, adap_telemetry = self.adaptive_compressor.compress_with_telemetry(text, config)
        comp_time = round((time.time() - c_t0) * 1000.0, 2)
        tot_time = round((time.time() - t0) * 1000.0, 2)

        telemetry.compression_time = comp_time
        telemetry.compression_time_ms = comp_time
        telemetry.number_of_llmlingua_calls = adap_telemetry["llmlingua_calls"]
        telemetry.number_of_adaptive_iterations = adap_telemetry["iterations"]
        telemetry.compression_attempts = adap_telemetry.get("compression_attempts", adap_telemetry["llmlingua_calls"])
        telemetry.validation_attempts = adap_telemetry.get("validation_attempts", adap_telemetry["iterations"])
        telemetry.retention_rates_attempted = adap_telemetry["retention_rates"]
        telemetry.validation_result_per_attempt = adap_telemetry["validation_results"]
        telemetry.validation_failure_reason = adap_telemetry["failure_reasons"]
        telemetry.fallback = (opt_res.compressed_text == text and orig_tokens > 20 and opt_res.status == 'failed')
        telemetry.fallback_reason = adap_telemetry.get("fallback_reason", "NONE")
        telemetry.final_token_count = opt_res.compressed_tokens
        telemetry.tokens_saved = max(0, orig_tokens - opt_res.compressed_tokens)
        telemetry.compression_percentage = opt_res.saving_percent
        telemetry.total_time = tot_time
        telemetry.total_time_ms = tot_time

        return opt_res, telemetry

    def optimize(self, text: str, mode: CompressionMode, category: str = "general", target_rate: Optional[float] = None, force_tokens: Optional[List[str]] = None) -> CompressionResult:
        return self.optimize_with_telemetry(text, mode=mode, category=category, target_rate=target_rate, force_tokens=force_tokens)[0]
