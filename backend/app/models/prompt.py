from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class CompressionMode(str, Enum):
    safe = 'safe'
    balanced = 'balanced'
    aggressive = 'aggressive'

class CompressionConfig(BaseModel):
    mode: CompressionMode
    target_rate: Optional[float] = None
    force_tokens: Optional[List[str]] = None
    target_model: Optional[str] = None

class PromptInput(BaseModel):
    text: str
    config: Optional[CompressionConfig] = None

class SegmentType(str, Enum):
    role = 'role'
    task = 'task'
    instruction = 'instruction'
    constraint = 'constraint'
    output_requirement = 'output_requirement'
    example = 'example'
    context = 'context'
    user_data = 'user_data'
    structured_content = 'structured_content'
    unknown = 'unknown'

class PromptSegment(BaseModel):
    text: str
    segment_type: SegmentType
    confidence: float = 1.0

class ParsedPrompt(BaseModel):
    original_text: str
    segments: List[PromptSegment]

class ConstraintType(str, Enum):
    prohibition = 'prohibition'
    quantity = 'quantity'
    style = 'style'
    unknown = 'unknown'

class ExtractedConstraint(BaseModel):
    raw_text: str
    constraint_type: ConstraintType
    details: dict = {}
    high_risk: bool = False


