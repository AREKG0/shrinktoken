from pydantic import BaseModel

class CostResult(BaseModel):
    """Cost result model. Implementation planned for Phase N."""
    original_cost: float
    optimized_cost: float
    compression_overhead: float
    net_saving: float
    currency: str
