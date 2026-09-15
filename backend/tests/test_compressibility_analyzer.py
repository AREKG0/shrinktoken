import pytest
from backend.app.compression.compressibility_analyzer import CompressibilityAnalyzer

class TestCompressibilityAnalyzer:
    def setup_method(self):
        self.analyzer = CompressibilityAnalyzer(min_token_savings=3, min_compressible_length=20)

    def test_short_prompt_early_exit(self):
        res = self.analyzer.analyze("Do not ask me questions.", category="negation")
        assert res["compressible"] is False
        assert res["recommended_strategy"] == "passthrough"
        assert "below minimum" in res["reason"] or "high risk" in res["reason"]

    def test_json_category_early_exit(self):
        text = '{"host": "127.0.0.1", "port": 5432, "database": "prod_db", "max_connections": 20}'
        res = self.analyzer.analyze(text, category="json")
        assert res["compressible"] is False
        assert res["recommended_strategy"] == "passthrough"

    def test_rag_category_compressible(self):
        text = "Context: SLA guarantees 99.99% uptime with maximum 4.38 minutes monthly downtime. " * 3
        res = self.analyzer.analyze(text, category="rag")
        assert res["compressible"] is True
        assert res["recommended_strategy"] == "rag_selective_compression"

    def test_multi_constraint_category_compressible(self):
        text = "Act as a security consultant. Review the authentication flow. Do not recommend basic auth. Provide exactly 3 recommendations. Format as a Markdown list. Keep response under 300 words. Do not ask questions."
        res = self.analyzer.analyze(text, category="multi_constraint")
        assert res["compressible"] is True
        assert res["risk_level"] == "HIGH"
