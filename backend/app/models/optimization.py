from pydantic import BaseModel
from typing import Literal

class CompressionResult(BaseModel):
    original_text: str
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    saving_percent: float
    mode_used: str
    status: Literal['safe', 'warning', 'failed']
