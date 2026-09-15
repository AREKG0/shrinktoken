import sys
from typing import Dict, Any, List

class BenchmarkIntegrityError(Exception):
    """Custom exception raised when benchmark aggregate statistics fail to reconcile."""
    pass

class BenchmarkIntegrityChecker:
    """
    Automated Benchmark Integrity Auditor for Phase 6.75.
    Mathematically verifies that all prompt evaluations, token counts, category breakdowns,
    fallback counts, false-pass counts, and model call limits strictly reconcile.
    """

    MAX_MODEL_CALLS_LIMIT = 4
    EXPECTED_TOTAL_PROMPTS = 405

    def check_integrity(self, summary: Dict[str, Any], results: List[Dict[str, Any]], prompts: List[Dict[str, Any]]) -> bool:
        errors = []

        # 1. Prompt evaluation count verification
        if len(prompts) != self.EXPECTED_TOTAL_PROMPTS:
            errors.append(f"Prompt dataset size mismatch: expected {self.EXPECTED_TOTAL_PROMPTS}, got {len(prompts)}")

        if len(results) != len(prompts):
            errors.append(f"Results prompt count mismatch: expected {len(prompts)}, got {len(results)}")

        # 2. Check unique prompt IDs and no duplicates
        seen_ids = set()
        for p in prompts:
            p_id = p.get("id")
            if not p_id or p_id in seen_ids:
                errors.append(f"Duplicate or empty prompt ID detected: '{p_id}'")
            seen_ids.add(p_id)

        # 3. Category count reconciliation
        cat_counts_sum = 0
        cat_orig_tokens_sum = 0
        cat_opt_tokens_sum = 0
        cat_fallbacks_sum = 0
        cat_fails_sum = 0

        category_breakdown = summary.get("category_breakdown", {})
        for cat, cstats in category_breakdown.items():
            cat_counts_sum += cstats.get("prompt_count", 0)
            cat_fallbacks_sum += cstats.get("fallbacks", 0)
            cat_fails_sum += cstats.get("validation_failures", 0)

        if cat_counts_sum != len(results):
            errors.append(f"Category prompt counts sum ({cat_counts_sum}) does not equal total prompts ({len(results)})")

        if summary.get("dataset_total_prompts") != len(results):
            errors.append(f"Summary total prompts ({summary.get('dataset_total_prompts')}) does not equal result length ({len(results)})")

        if summary.get("fallbacks") != cat_fallbacks_sum:
            errors.append(f"Summary fallbacks ({summary.get('fallbacks')}) does not equal category fallbacks sum ({cat_fallbacks_sum})")

        if summary.get("failed") != cat_fails_sum:
            errors.append(f"Summary validation failures ({summary.get('failed')}) does not equal category failures sum ({cat_fails_sum})")

        # 4. Token count mathematical reconciliation
        total_orig = sum(r.get("original_tokens", 0) for r in results)
        total_opt = sum(r.get("optimized_tokens", 0) for r in results)
        total_saved = total_orig - total_opt

        if summary.get("total_original_tokens") != total_orig:
            errors.append(f"Summary total original tokens ({summary.get('total_original_tokens')}) != sum of result original tokens ({total_orig})")

        if summary.get("total_optimized_tokens") != total_opt:
            errors.append(f"Summary total optimized tokens ({summary.get('total_optimized_tokens')}) != sum of result optimized tokens ({total_opt})")

        if summary.get("total_tokens_saved") != total_saved:
            errors.append(f"Summary total tokens saved ({summary.get('total_tokens_saved')}) != calculated saved tokens ({total_saved})")

        # 5. Model call cap & fallback text integrity
        for r in results:
            calls = r.get("llmlingua_calls", 0)
            if calls > self.MAX_MODEL_CALLS_LIMIT:
                errors.append(f"Prompt {r.get('id')} exceeded max model calls: {calls} > {self.MAX_MODEL_CALLS_LIMIT}")

            if r.get("fallback") is True:
                orig_t = r.get("original_text")
                opt_t = r.get("optimized_text")
                if orig_t != opt_t:
                    errors.append(f"Prompt {r.get('id')} has fallback=True but optimized_text != original_text")

            if r.get("early_exit") is True:
                if r.get("llmlingua_calls") != 0:
                    errors.append(f"Prompt {r.get('id')} has early_exit=True but model_calls = {r.get('llmlingua_calls')}")

        # 6. False-pass & false-fail attribution
        fp_list = summary.get("false_passes", [])
        for fp in fp_list:
            if fp.get("category") != "adversarial":
                errors.append(f"False pass reported for non-adversarial category: {fp}")

        if errors:
            err_msg = "BENCHMARK INTEGRITY RECONCILIATION FAILED:\n" + "\n".join(f" - {e}" for e in errors)
            print(err_msg, file=sys.stderr)
            raise BenchmarkIntegrityError(err_msg)

        print(f"Benchmark integrity check PASSED cleanly for all {len(results)} prompts.")
        return True
