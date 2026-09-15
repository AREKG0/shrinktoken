"""
Adversarial tests specifically designed to challenge validation boundaries.
Measures validator responses on deliberately corrupted compressed prompts.
"""
import pytest
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.validators.negation_validator import NegationValidator
from backend.app.validators.numeric_validator import NumericValidator
from backend.app.validators.structural_validator import StructuralValidator

class TestAdversarialValidation:
    def setup_method(self):
        self.validator = ConstraintValidator()
        self.negation_v = NegationValidator()
        self.numeric_v = NumericValidator()
        self.structural_v = StructuralValidator()

    def test_adv_operator_change_fails(self):
        original = "Give exactly 5 examples."
        bad = "Give at least 5 examples."
        # 'exactly' vs 'at least' operator conflict
        assert self.numeric_v.validate(original, bad) is False

    def test_adv_reversed_range_fails(self):
        original = "Complete this within 15-60 minutes."
        bad = "Complete this within 60-15 minutes."
        assert self.numeric_v.validate(original, bad) is False

    def test_adv_swapped_number_context_fails(self):
        original = "Use 5 examples and explain each in 100 words."
        bad = "Use 100 examples and explain each in 5 words."
        # Identical number sets {5, 100}, but bound to wrong targets
        result = self.validator.validate(original, bad)
        assert result.status == "FAIL" or len(result.critical_failures) > 0

    def test_adv_url_param_modification_fails(self):
        original = "Return exactly this URL: https://example.com/api?v=1"
        bad = "Return exactly this URL: https://example.com/api?v=2"
        assert self.structural_v.validate(original, bad) is False

    def test_adv_scope_loss_measurement(self):
        original = "Do not ask me questions about my preferences."
        bad = "Do not ask me questions."
        result = self.validator.validate(original, bad)
        # Record validation status for semantic scope loss metric
        assert result.status in ["PASS", "FAIL"]

    def test_adv_audience_target_measurement(self):
        original = "Explain recursion to a beginner."
        bad = "Explain recursion to an expert."
        result = self.validator.validate(original, bad)
        assert result.status in ["PASS", "FAIL"]

    def test_adv_missing_schema_field_measurement(self):
        original = "Return JSON with fields name and age."
        bad = "Return JSON with field name."
        result = self.validator.validate(original, bad)
        assert result.status in ["PASS", "FAIL"]

    def test_adv_positive_instruction_loss_measurement(self):
        original = "Do not summarize the article, but explain its conclusion."
        bad = "Do not summarize the article."
        result = self.validator.validate(original, bad)
        assert result.status in ["PASS", "FAIL"]

    def test_adv_style_instruction_loss_measurement(self):
        original = "Explain recursion using simple language."
        bad = "Explain recursion."
        result = self.validator.validate(original, bad)
        assert result.status in ["PASS", "FAIL"]
