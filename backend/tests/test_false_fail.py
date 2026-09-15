"""
Test suite to track and measure False Fail cases across validators.
A False Fail occurs when a validator rejects (returns False/FAIL) a compressed prompt that
is actually semantically equivalent and preserves intended constraints.
"""
import pytest
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.validators.negation_validator import NegationValidator
from backend.app.validators.numeric_validator import NumericValidator

class TestFalseFailMetrics:
    def setup_method(self):
        self.validator = ConstraintValidator()
        self.negation_v = NegationValidator()
        self.numeric_v = NumericValidator()

    def test_synonym_negation_preservation(self):
        """
        Original: "Do not ask me questions."
        Compressed: "Please refrain from asking questions."
        Expected: PASS (synonymous prohibition)
        """
        original = "Do not ask me questions."
        compressed = "Please refrain from asking questions."
        # Negation validator check
        is_valid = self.negation_v.validate(original, compressed)
        assert is_valid, "FALSE FAIL DETECTED: Validator rejected synonymous negation 'refrain from'"

    def test_spelled_out_number_preservation(self):
        """
        Original: "Give exactly 5 examples."
        Compressed: "Provide precisely five examples."
        Expected: PASS (word number 'five' equivalent to '5')
        """
        original = "Give exactly 5 examples."
        compressed = "Provide precisely five examples."
        is_valid = self.numeric_v.validate(original, compressed)
        assert is_valid, "FALSE FAIL DETECTED: Validator rejected word number 'five'"
