"""
Test suite to track and measure False Pass cases across validators.
A False Pass occurs when a validator approves (returns True/PASS) a prompt that has been
deliberately corrupted or altered in meaning.
"""
import pytest
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.validators.numeric_validator import NumericValidator
from backend.app.validators.negation_validator import NegationValidator

class TestFalsePassMetrics:
    def setup_method(self):
        self.validator = ConstraintValidator()
        self.numeric_v = NumericValidator()
        self.negation_v = NegationValidator()

    def test_false_pass_swapped_numeric_targets(self):
        """
        Original: "Use 5 examples and explain each in 100 words."
        Corrupted: "Use 100 examples and explain each in 5 words."
        Expected: Validation must reject this.
        """
        original = "Use 5 examples and explain each in 100 words."
        corrupted = "Use 100 examples and explain each in 5 words."
        result = self.validator.validate(original, corrupted)
        # Tracking if validator approves this false pass
        is_false_pass = (result.status == "PASS")
        assert not is_false_pass, "FALSE PASS DETECTED: Validator approved swapped numeric targets"

    def test_false_pass_swapped_dimensions(self):
        """
        Original: "Format matrix as 4 rows and 10 columns."
        Corrupted: "Format matrix as 10 rows and 4 columns."
        Expected: Validation must reject this.
        """
        original = "Format matrix as 4 rows and 10 columns."
        corrupted = "Format matrix as 10 rows and 4 columns."
        result = self.validator.validate(original, corrupted)
        is_false_pass = (result.status == "PASS")
        assert not is_false_pass, "FALSE PASS DETECTED: Validator approved swapped matrix dimensions"
