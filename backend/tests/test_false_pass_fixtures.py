"""
Regression test suite for all 17 false passes discovered in Phase 4 benchmark.
Ensures every identified vulnerability is permanently tested and rejected.
"""
import json
import os
import pytest
from backend.app.validators.constraint_validator import ConstraintValidator

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "false_passes.json")

def load_fixtures():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

class TestFalsePassFixtures:
    def setup_method(self):
        self.validator = ConstraintValidator()

    @pytest.mark.parametrize("item", load_fixtures(), ids=lambda x: x["id"])
    def test_false_pass_fixture_fails(self, item):
        orig = item["original"]
        bad = item["unsafe_compressed"]
        res = self.validator.validate(orig, bad)
        assert res.status == "FAIL" or len(res.critical_failures) > 0, (
            f"Fixture {item['id']} ({item['failure_type']}) unexpectedly passed!\n"
            f"Original: {orig}\nUnsafe: {bad}\nResult: {res}"
        )
