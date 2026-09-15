"""
Test suite for conditional constraint validation.
Verifies that clauses containing conditional triggers (unless, except, provided that, only if)
are recognized as compound constraints and not partially dropped.
"""
import pytest
from backend.app.validators.negation_validator import NegationValidator
from backend.app.validators.constraint_validator import ConstraintValidator

class TestConditionalConstraints:
    def setup_method(self):
        self.negation_v = NegationValidator()
        self.validator = ConstraintValidator()

    def test_unless_condition_dropped_detected(self):
        original = "Do not ask questions unless clarification is required."
        corrupted = "Do not ask questions."
        result = self.validator.validate(original, corrupted)
        assert result.status in ["FAIL", "WARNING"] or len(result.warnings) > 0

    def test_except_condition_dropped_detected(self):
        original = "Never mention competitor products except when explicitly requested."
        corrupted = "Never mention competitor products."
        result = self.validator.validate(original, corrupted)
        assert result.status in ["FAIL", "WARNING"] or len(result.warnings) > 0

    def test_only_if_condition_preserved(self):
        original = "Only use external sources if necessary."
        compressed = "Only use external sources if necessary."
        result = self.validator.validate(original, compressed)
        assert result.status == "PASS"
