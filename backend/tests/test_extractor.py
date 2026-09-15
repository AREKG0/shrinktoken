from backend.app.models.prompt import ConstraintType
from backend.app.services.instruction_extractor import InstructionExtractor

def test_instruction_extractor_prohibition():
    extractor = InstructionExtractor()
    result = extractor.extract("Do not ask me questions.")
    assert len(result) == 1
    assert result[0].constraint_type == ConstraintType.prohibition
    assert result[0].details["action"] == "ask me questions"
    assert result[0].details["polarity"] == "negative"

def test_instruction_extractor_quantity():
    extractor = InstructionExtractor()
    result = extractor.extract("Give exactly 5 examples.")
    assert len(result) == 1
    assert result[0].constraint_type == ConstraintType.quantity
    assert result[0].details["operator"] == "exactly"
    assert result[0].details["value"] == 5
    assert result[0].details["target"] == "examples"

def test_instruction_extractor_style():
    extractor = InstructionExtractor()
    result = extractor.extract("Use simple language please.")
    assert len(result) == 1
    assert result[0].constraint_type == ConstraintType.style
    assert result[0].details["requirement"] == "simple language"

def test_instruction_extractor_unknown():
    extractor = InstructionExtractor()
    result = extractor.extract("Make sure you write with a green pen unless it is a Sunday.")
    assert len(result) == 1
    assert result[0].constraint_type == ConstraintType.unknown
    assert result[0].high_risk is True
