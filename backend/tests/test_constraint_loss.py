"""
Test suite to verify detection of instruction and constraint loss.
Verifies that when a prompt's style, restriction, or specific instruction is dropped during compression,
the validator detects the loss.
"""
import pytest
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.services.instruction_extractor import InstructionExtractor

class TestConstraintLoss:
    def setup_method(self):
        self.validator = ConstraintValidator()
        self.extractor = InstructionExtractor()

    def test_style_instruction_loss_flagged(self):
        original = "Explain recursion to a beginner using simple language."
        corrupted = "Explain recursion."
        result = self.validator.validate(original, corrupted)
        assert result.status in ["FAIL", "WARNING"] or len(result.warnings) > 0

    def test_prohibition_instruction_loss_flagged(self):
        original = "Explain recursion but do not use code."
        corrupted = "Explain recursion."
        result = self.validator.validate(original, corrupted)
        assert result.status == "FAIL"

    def test_quantity_instruction_loss_flagged(self):
        original = "Explain recursion and provide 3 examples."
        corrupted = "Explain recursion."
        result = self.validator.validate(original, corrupted)
        assert result.status == "FAIL"
