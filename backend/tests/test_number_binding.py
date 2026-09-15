"""
Tests for Number-to-Context Binding in NumericValidator.
Verifies that number values remain bound to their target entities/words
and cannot be arbitrarily swapped across targets even if the number set is identical.
"""
import pytest
from backend.app.validators.numeric_validator import NumericValidator

class TestNumberBinding:
    def setup_method(self):
        self.validator = NumericValidator()

    def test_swapped_values_and_targets_rejected(self):
        original = "Use 5 examples and explain each in 100 words."
        corrupted = "Use 100 examples and explain each in 5 words."
        assert self.validator.validate(original, corrupted) is False

    def test_exact_binding_preserved(self):
        original = "Use 5 examples and explain each in 100 words."
        compressed = "Provide 5 examples of 100 words each."
        assert self.validator.validate(original, compressed) is True

    def test_swapped_multi_target_numbers_rejected(self):
        original = "Allocate 3 nodes with 16GB RAM and 500GB storage."
        corrupted = "Allocate 16 nodes with 500GB RAM and 3GB storage."
        assert self.validator.validate(original, corrupted) is False

    def test_swapped_dimensions_rejected(self):
        original = "Format matrix as 4 rows and 10 columns."
        corrupted = "Format matrix as 10 rows and 4 columns."
        assert self.validator.validate(original, corrupted) is False
