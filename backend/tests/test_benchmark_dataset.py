"""
Validation tests for Phase 4 benchmark dataset integrity.
Ensures all JSON benchmark files are valid, conform to schema, and contain required categories.
"""
import json
import glob
import os
import pytest

BENCHMARK_DIR = os.path.join(os.path.dirname(__file__), "..", "benchmarks", "prompts")

def test_benchmark_files_exist():
    files = glob.glob(os.path.join(BENCHMARK_DIR, "*.json"))
    assert len(files) >= 13, f"Expected at least 13 benchmark files, found {len(files)}"

def test_benchmark_prompts_valid_json_schema():
    files = glob.glob(os.path.join(BENCHMARK_DIR, "*.json"))
    total_prompts = 0
    categories = set()
    
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, list), f"{filepath} must contain a JSON array"
            for item in data:
                assert "id" in item, f"Missing 'id' in {item}"
                assert "category" in item, f"Missing 'category' in {item}"
                assert "prompt" in item, f"Missing 'prompt' in {item}"
                categories.add(item["category"])
                total_prompts += 1

    assert total_prompts >= 120, f"Expected 120+ benchmark items, found {total_prompts}"
    assert len(categories) >= 12, f"Expected 12+ categories, found {len(categories)}"
