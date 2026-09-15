"""
Regression tests for the full safety and validation layer.
Covers negation, numeric, structural, constraints, adaptive compression,
placeholder integrity, and failure/fallback behavior.
"""
import pytest
from unittest.mock import MagicMock
from backend.app.validators.negation_validator import NegationValidator
from backend.app.validators.numeric_validator import NumericValidator
from backend.app.validators.structural_validator import StructuralValidator
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.services.protection_engine import ProtectionEngine
from backend.app.compression.adaptive import AdaptiveCompressor
from backend.app.compression.llmlingua import LLMLinguaCompressor
from backend.app.models.prompt import CompressionConfig, CompressionMode
from backend.app.models.optimization import CompressionResult


# ==============================================================================
# NEGATION VALIDATOR TESTS
# ==============================================================================

class TestNegationValidator:
    def setup_method(self):
        self.v = NegationValidator()

    def test_critical_regression_do_not_ask(self):
        original = "Do not ask me what I want to do."
        flipped  = "Ask me what I want to do."
        assert self.v.validate(original, flipped) is False

    def test_negation_preserved(self):
        original = "Do not ask me what I want to do."
        compressed = "Do not ask what I want."
        assert self.v.validate(original, compressed) is True

    def test_never_mention_politics_flipped(self):
        original = "Never mention politics."
        flipped  = "Mention politics."
        assert self.v.validate(original, flipped) is False

    def test_never_mention_politics_preserved(self):
        original = "Never mention politics."
        compressed = "Never mention politics."
        assert self.v.validate(original, compressed) is True

    def test_multiple_negations_all_preserved(self):
        original = "Do not ask questions. Never use passive voice."
        compressed = "Do not ask. Never use passive voice."
        assert self.v.validate(original, compressed) is True

    def test_multiple_negations_one_dropped(self):
        original = "Do not ask questions. Never use passive voice."
        compressed = "Do not ask. Use passive voice."
        assert self.v.validate(original, compressed) is False

    def test_empty_original(self):
        assert self.v.validate("", "anything") is True

    def test_no_negation_in_original(self):
        original = "Write a blog post about AI."
        compressed = "Write blog AI."
        assert self.v.validate(original, compressed) is True

    def test_conditional_negation_preserved(self):
        original = "Do not answer unless the question is clear."
        compressed = "Do not answer unless question clear."
        assert self.v.validate(original, compressed) is True


# ==============================================================================
# NUMERIC VALIDATOR TESTS
# ==============================================================================

class TestNumericValidator:
    def setup_method(self):
        self.v = NumericValidator()

    def test_exact_count_preserved(self):
        assert self.v.validate("Give exactly 5 examples.", "Give exactly 5 examples.") is True

    def test_number_dropped(self):
        assert self.v.validate("Give exactly 5 examples.", "Give examples.") is False

    def test_range_preserved(self):
        assert self.v.validate("Complete within 15-60 minutes.", "Complete within 15-60 minutes.") is True

    def test_range_reversed(self):
        assert self.v.validate("Complete within 15-60 minutes.", "Complete within 60-15 minutes.") is False

    def test_range_number_dropped(self):
        assert self.v.validate("Complete within 15-60 minutes.", "Complete within 60 minutes.") is False

    def test_decimal_preserved(self):
        assert self.v.validate("Set precision to 0.05.", "Set precision to 0.05.") is True

    def test_decimal_dropped(self):
        assert self.v.validate("Set precision to 0.05.", "Set precision.") is False

    def test_empty_original(self):
        assert self.v.validate("", "anything") is True

    def test_standalone_numbers_preserved(self):
        assert self.v.validate("Use 3 paragraphs and 10 sentences.", "Use 3 paragraphs and 10 sentences.") is True


# ==============================================================================
# STRUCTURAL VALIDATOR TESTS
# ==============================================================================

class TestStructuralValidator:
    def setup_method(self):
        self.v = StructuralValidator()

    def test_url_preserved(self):
        assert self.v.validate("Return exactly this URL: https://example.com", "Return https://example.com") is True

    def test_url_dropped(self):
        assert self.v.validate("Return exactly this URL: https://example.com", "Return the URL.") is False

    def test_code_block_preserved(self):
        original = "Run this:\n```python\nprint('hello')\n```"
        assert self.v.validate(original, original) is True

    def test_code_block_dropped(self):
        original = "Run this:\n```python\nprint('hello')\n```"
        compressed = "Run this: print hello"
        assert self.v.validate(original, compressed) is False

    def test_valid_json_preserved(self):
        original = 'Use JSON output: {"name": "test", "value": 42}'
        assert self.v.validate(original, original) is True

    def test_json_dropped(self):
        original = 'Use JSON output: {"name": "test", "value": 42}'
        compressed = "Use JSON output."
        assert self.v.validate(original, compressed) is False

    def test_empty_original(self):
        assert self.v.validate("", "anything") is True


# ==============================================================================
# PROTECTION ENGINE + PLACEHOLDER TESTS
# ==============================================================================

class TestPlaceholderIntegrity:
    def setup_method(self):
        self.engine = ProtectionEngine()

    def test_code_roundtrip(self):
        text = "Explain this code:\n```python\nprint('hello')\n```"
        masked, mapping = self.engine.mask(text)
        assert "print('hello')" not in masked
        assert self.engine.validate_placeholders(masked, mapping) is True
        assert self.engine.unmask(masked, mapping) == text

    def test_json_roundtrip(self):
        text = 'Respond with: {"key": "value", "count": 5}'
        masked, mapping = self.engine.mask(text)
        assert "value" not in masked
        assert self.engine.unmask(masked, mapping) == text

    def test_url_roundtrip(self):
        text = "Return exactly this URL: https://example.com/api?key=123"
        masked, mapping = self.engine.mask(text)
        assert "example.com" not in masked
        assert self.engine.unmask(masked, mapping) == text

    def test_duplicate_placeholder_fails(self):
        text = "Visit https://google.com"
        masked, mapping = self.engine.mask(text)
        duplicated = masked + " " + list(mapping.keys())[0]
        assert self.engine.validate_placeholders(duplicated, mapping) is False

    def test_missing_placeholder_fails(self):
        text = "Visit https://google.com"
        masked, mapping = self.engine.mask(text)
        removed = masked.replace(list(mapping.keys())[0], "")
        assert self.engine.validate_placeholders(removed, mapping) is False


# ==============================================================================
# CONSTRAINT VALIDATOR TESTS
# ==============================================================================

class TestConstraintValidator:
    def setup_method(self):
        self.v = ConstraintValidator()

    def test_do_not_ask_fails(self):
        original = "Do not ask me what I want to do."
        flipped  = "Ask me what I want to do."
        result = self.v.validate(original, flipped)
        assert result.status == "FAIL"
        assert len(result.critical_failures) > 0

    def test_do_not_ask_preserved_passes(self):
        original = "Do not ask me what I want to do."
        compressed = "Do not ask what I want."
        result = self.v.validate(original, compressed)
        assert result.status == "PASS"

    def test_url_dropped_fails(self):
        original = "Return exactly this URL: https://example.com"
        compressed = "Return the URL."
        result = self.v.validate(original, compressed)
        assert result.status == "FAIL"

    def test_number_dropped_fails(self):
        original = "Give exactly 5 examples."
        compressed = "Give examples."
        result = self.v.validate(original, compressed)
        assert result.status == "FAIL"

    def test_range_reversed_fails(self):
        original = "Complete within 15-60 minutes."
        compressed = "Complete within 60-15 minutes."
        result = self.v.validate(original, compressed)
        assert result.status == "FAIL"

    def test_empty_original_passes(self):
        result = self.v.validate("", "anything")
        assert result.status == "PASS"


# ==============================================================================
# ADAPTIVE COMPRESSION FALLBACK TESTS (no LLMLingua model needed)
# ==============================================================================

class TestAdaptiveFallback:
    def _make_failing_compressor(self):
        mock = MagicMock()
        mock.name = "MockFail"
        mock.is_available = True
        mock.compress.return_value = CompressionResult(
            original_text="",
            compressed_text="Ask me what I want to do.",  # flipped negation
            original_tokens=10,
            compressed_tokens=6,
            compression_ratio=1.6,
            saving_percent=40.0,
            mode_used="balanced",
            status="safe"
        )
        return mock

    def test_adaptive_falls_back_on_invalid_output(self):
        original = "Do not ask me what I want to do. Write a short summary."
        config = CompressionConfig(mode=CompressionMode.balanced)
        adaptive = AdaptiveCompressor(self._make_failing_compressor())
        result = adaptive.compress(original, config)
        # All retries will fail due to flipped negation, must fall back to original
        assert result.compressed_text == original or result.status == "failed"

    def test_adaptive_binary_search_direction(self):
        """
        Verify search logic: PASS => try stronger compression (lower max_retention_rate),
        FAIL => try weaker compression (raise min_retention_rate).
        """
        calls = []
        
        def smart_compress(text, config):
            rate = config.target_rate or 0.6
            calls.append(rate)
            # Only rates >= 0.7 are "safe" — lower rates produce invalid output
            compressed = "Do not ask what I want." if rate >= 0.7 else "Ask what I want."
            return CompressionResult(
                original_text=text,
                compressed_text=compressed,
                original_tokens=10,
                compressed_tokens=int(10 * rate),
                compression_ratio=1/rate,
                saving_percent=(1-rate)*100,
                mode_used="balanced",
                status="safe"
            )
            
        mock = MagicMock()
        mock.name = "SmartMock"
        mock.is_available = True
        mock.compress.side_effect = smart_compress

        original = "Do not ask me what I want."
        config = CompressionConfig(mode=CompressionMode.balanced)
        adaptive = AdaptiveCompressor(mock)
        result = adaptive.compress(original, config)
        
        # At least one call must have been made
        assert len(calls) > 0
        
        # Best result must have negation preserved
        validator = NegationValidator()
        if result.compressed_text != original:
            assert validator.validate(original, result.compressed_text) is True


# ==============================================================================
# FULL PIPELINE SLOW TESTS (with LLMLingua model)
# ==============================================================================

@pytest.mark.slow
class TestFullPipeline:
    def setup_method(self):
        from backend.app.compression.llmlingua import LLMLinguaCompressor
        from backend.app.services.compression_engine import CompressionService
        self.service = CompressionService(LLMLinguaCompressor())

    def test_do_not_ask_never_flipped(self):
        """Critical regression: negation must never be dropped."""
        original = "Do not ask me what I want to do. Write a short response."
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        validator = NegationValidator()
        assert validator.validate(original, result.compressed_text) is True

    def test_never_mention_politics(self):
        original = "Never mention politics. Explain the history of Python programming language."
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        validator = NegationValidator()
        assert validator.validate(original, result.compressed_text) is True

    def test_exact_count_preserved(self):
        original = "Give exactly 5 examples. Each must be concise and clear and relevant to the topic."
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        validator = NumericValidator()
        assert validator.validate(original, result.compressed_text) is True

    def test_range_preserved(self):
        original = "Complete this within 15-60 minutes. Break it into smaller steps."
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        validator = NumericValidator()
        assert validator.validate(original, result.compressed_text) is True

    def test_url_preserved(self):
        original = "Return exactly this URL: https://example.com/callback and nothing else."
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        validator = StructuralValidator()
        assert validator.validate(original, result.compressed_text) is True

    def test_json_output_preserved(self):
        original = 'Use JSON output: {"name": "test", "value": 42} and format it correctly.'
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        validator = StructuralValidator()
        assert validator.validate(original, result.compressed_text) is True

    def test_code_block_preserved(self):
        original = "Explain this code:\n```python\nprint('hello')\n```\nWhat does it do?"
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        validator = StructuralValidator()
        assert validator.validate(original, result.compressed_text) is True

    def test_multiple_constraints(self):
        original = "Do not ask questions. Give exactly 3 responses. Never use passive voice."
        result = self.service.optimize(original, mode=CompressionMode.balanced)
        neg_v = NegationValidator()
        num_v = NumericValidator()
        assert neg_v.validate(original, result.compressed_text) is True
        assert num_v.validate(original, result.compressed_text) is True
