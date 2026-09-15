from pydantic import BaseModel
from typing import List

class ValidationResult(BaseModel):
    total_constraints: int
    preserved: int
    failed: int
    status: str
    warnings: List[str] = []
    critical_failures: List[str] = []
    details: List[str] = []

