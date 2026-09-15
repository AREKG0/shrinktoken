from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class OptimizationTelemetry(BaseModel):
    request_id: str = ""
    prompt_id: str = ""
    category: str = "general"
    original_token_count: int = 0
    final_token_count: int = 0
    tokens_saved: int = 0
    compression_percentage: float = 0.0
    number_of_llmlingua_calls: int = 0
    number_of_adaptive_iterations: int = 0
    validation_attempts: int = 0
    compression_attempts: int = 0
    retention_rates_attempted: List[float] = []
    validation_result_per_attempt: List[str] = []
    validation_failure_reason: List[str] = []
    validation_status: str = "PASS"
    validation_failures: List[str] = []
    fallback: bool = False
    fallback_reason: str = "NONE"
    early_exit: bool = False
    early_exit_reason: str = ""
    protection_time: float = 0.0
    compression_time: float = 0.0
    validation_time: float = 0.0
    total_time: float = 0.0
    protection_time_ms: float = 0.0
    compression_time_ms: float = 0.0
    validation_time_ms: float = 0.0
    total_time_ms: float = 0.0

    def dict_without_sensitive_text(self) -> Dict[str, Any]:
        """JSON serializable telemetry output excluding raw prompt text."""
        return self.model_dump()
