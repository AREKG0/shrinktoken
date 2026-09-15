from typing import Optional
from backend.app.compression.base import BaseCompressor
from backend.app.models.prompt import CompressionConfig, CompressionMode
from backend.app.models.optimization import CompressionResult
from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)

class LLMLinguaCompressor(BaseCompressor):
    def __init__(self):
        self._compressor = None
        
    @property
    def name(self) -> str:
        return "LLMLingua-2"
        
    @property
    def is_available(self) -> bool:
        return True
        
    def _get_compressor(self):
        if self._compressor is None:
            logger.info("Initializing LLMLingua PromptCompressor...")
            try:
                from llmlingua import PromptCompressor
                self._compressor = PromptCompressor(
                    model_name=settings.LLMLINGUA_MODEL_NAME,
                    use_llmlingua2=True,
                    device_map=settings.DEVICE_MAP
                )
            except Exception as e:
                logger.error(f"Failed to initialize compressor: {e}")
                raise
        return self._compressor

    def get_token_count(self, text: str) -> int:
        if not text:
            return 0
        try:
            compressor = self._get_compressor()
            if hasattr(compressor, "tokenizer") and compressor.tokenizer is not None:
                return len(compressor.tokenizer.encode(text, add_special_tokens=False))
        except Exception:
            pass
        return len(text.split())

    def compress(self, text: str, config: CompressionConfig) -> CompressionResult:
        try:
            compressor = self._get_compressor()
            
            rate_map = {
                CompressionMode.safe: 0.8,
                CompressionMode.balanced: 0.6,
                CompressionMode.aggressive: 0.4
            }
            
            rate = config.target_rate if config.target_rate is not None else rate_map.get(config.mode, 0.6)
            force_tokens = config.force_tokens if config.force_tokens is not None else ['\\n', '?', '.', ':', '!', ';']
            
            result = compressor.compress_prompt(
                text,
                rate=rate,
                force_tokens=force_tokens
            )
            
            original_tokens = result.get("origin_tokens", self.get_token_count(text))
            compressed_tokens = result.get("compressed_tokens", self.get_token_count(result.get("compressed_prompt", "")))
            
            saving_percent = 0.0
            if original_tokens > 0:
                saving_percent = max(0.0, (1.0 - (compressed_tokens / original_tokens)) * 100.0)
                
            ratio_str = result.get("ratio", "1.0")
            if isinstance(ratio_str, str):
                ratio_str = ratio_str.replace("x", "")
            try:
                compression_ratio = float(ratio_str)
            except ValueError:
                compression_ratio = original_tokens / compressed_tokens if compressed_tokens > 0 else 1.0
            
            return CompressionResult(
                original_text=text,
                compressed_text=result.get("compressed_prompt", ""),
                original_tokens=original_tokens,
                compressed_tokens=compressed_tokens,
                compression_ratio=compression_ratio,
                saving_percent=saving_percent,
                mode_used=config.mode.value,
                status='safe'
            )
        except Exception as e:
            logger.error(f"Compression failed: {e}")
            tokens = self.get_token_count(text)
            return CompressionResult(
                original_text=text,
                compressed_text=text,
                original_tokens=tokens,
                compressed_tokens=tokens,
                compression_ratio=1.0,
                saving_percent=0.0,
                mode_used=config.mode.value,
                status='failed'
            )
