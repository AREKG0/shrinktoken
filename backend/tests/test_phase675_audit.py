import pytest
from backend.app.validators.format_validator import FormatValidator
from backend.app.validators.audience_validator import AudienceValidator
from backend.app.validators.negation_validator import NegationValidator
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.benchmarks.integrity_checker import BenchmarkIntegrityChecker, BenchmarkIntegrityError
from backend.app.compression.llmlingua import LLMLinguaCompressor
from backend.app.services.compression_engine import CompressionService
from backend.app.services.cost_engine import CostEngine
from backend.app.core.config import settings
from backend.app.models.prompt import CompressionMode

class TestPhase675Audit:
    """Comprehensive test suite for Phase 6.75 Audit & Safety Hardening."""

    def test_adv023_format_validator_fix(self):
        """ADV-023: 'Return only the final answer as a single floating point number.' vs corrupted candidate."""
        fmt_v = FormatValidator()
        orig = "Return only the final answer as a single floating point number."
        corrupted = "Return a long multi-paragraph explanation."
        
        spec_orig = fmt_v.extract_format_spec(orig)
        assert spec_orig["output_type"] == "floating_point_number"
        assert spec_orig["cardinality"] == 1
        assert spec_orig["restrictive"] is True

        spec_comp = fmt_v.extract_format_spec(corrupted)
        assert spec_comp["output_type"] == "paragraph"

        assert fmt_v.validate(orig, corrupted) is False, "FormatValidator must reject ADV-023 corrupted candidate"

    def test_adv001_scope_preservation_fix(self):
        """ADV-001: 'Do not ask me questions about my preferences.' vs corrupted candidate 'Do not ask me questions.'"""
        neg_v = NegationValidator()
        orig = "Do not ask me questions about my preferences."
        corrupted = "Do not ask me questions."

        # Target scope 'preferences' missing
        assert neg_v.validate(orig, corrupted) is False, "NegationValidator must reject ADV-001 target scope truncation"

    def test_audience_validator_drift(self):
        """AudienceValidator must reject persona/level drift (e.g. beginner -> expert)."""
        aud_v = AudienceValidator()
        orig = "Explain quantum computing to a beginner."
        corrupted = "Explain quantum computing to an expert."

        assert aud_v.validate(orig, corrupted) is False, "AudienceValidator must reject beginner -> expert drift"

    def test_benchmark_integrity_checker_raises_on_invalid_data(self):
        """BenchmarkIntegrityChecker must raise BenchmarkIntegrityError if stats do not reconcile."""
        checker = BenchmarkIntegrityChecker()
        invalid_summary = {
            "dataset_total_prompts": 405,
            "passed": 400,
            "failed": 5,
            "fallbacks": 10, # Mismatch!
            "total_original_tokens": 1000,
            "total_optimized_tokens": 900,
            "total_tokens_saved": 50, # Mismatch (1000-900 != 50)!
            "category_breakdown": {
                "general": {"prompt_count": 400, "fallbacks": 5, "validation_failures": 5}
            }
        }
        mock_results = [{"id": f"p-{i}", "category": "general"} for i in range(405)]
        mock_prompts = [{"id": f"p-{i}", "category": "general"} for i in range(405)]

        with pytest.raises(BenchmarkIntegrityError):
            checker.check_integrity(invalid_summary, mock_results, mock_prompts)

    def test_fallback_exact_match_assertion(self):
        """When fallback is triggered, output text MUST strictly equal original text."""
        compressor = LLMLinguaCompressor()
        service = CompressionService(compressor, max_model_calls=settings.MAX_MODEL_CALLS)
        
        # High constraint prompt that fails aggressive compression
        text = "Return valid JSON containing keys 'id' and 'name' with no additional explanations or markdown text."
        res, telemetry = service.optimize_with_telemetry(text, mode=CompressionMode.balanced, category="json")

        if telemetry.fallback:
            assert res.compressed_text == text, "Fallback output text must strictly match original text"

    def test_tokenizer_consistency_urls_json_code(self):
        """Verify XLM-RoBERTa subword tokenizer counts tokens consistently for URLs, JSON, and Code."""
        compressor = LLMLinguaCompressor()
        
        url_prompt = "Visit https://api.example.com/v1/data?query=test&format=json"
        json_prompt = '{"name": "test", "items": [1, 2, 3]}'
        code_prompt = "def hello(): print('world')"

        count_url = compressor.get_token_count(url_prompt)
        count_json = compressor.get_token_count(json_prompt)
        count_code = compressor.get_token_count(code_prompt)

        assert count_url > 0
        assert count_json > 0
        assert count_code > 0
        assert count_url != len(url_prompt.split()), "Tokenizer must use subword tokens, not whitespace word counts"

    def test_cost_engine_configurable_inputs(self):
        """CostEngine calculates benchmark baseline, optimized, and gross dollar savings."""
        engine = CostEngine()
        res = engine.calculate(
            original_input_tokens=1000,
            optimized_input_tokens=800,
            provider_input_price_per_million=2.50,
            number_of_requests=1000
        )
        assert res.original_cost == 2.50
        assert res.optimized_cost == 2.00
        assert res.net_saving == 0.50
