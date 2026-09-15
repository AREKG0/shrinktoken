"""
Metrics calculation module for ShrinkToken Pro benchmarks (Phase 6.5).
Computes Macro Average, Corpus-Weighted Reduction, LLMLingua calls per prompt,
latency by model call count, percentiles, and category telemetry.
"""
import math
from typing import Dict, Any, List

def percentile(data: List[float], pct: float) -> float:
    if not data:
        return 0.0
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n == 1:
        return sorted_data[0]
    pos = (n - 1) * (pct / 100.0)
    idx = int(pos)
    frac = pos - idx
    if idx >= n - 1:
        return sorted_data[-1]
    return sorted_data[idx] + frac * (sorted_data[idx + 1] - sorted_data[idx])

def compute_benchmark_summary(results: List[Dict[str, Any]], false_pass_list: List[Dict[str, Any]] = None, false_fail_list: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    total_prompts = len(results)
    if total_prompts == 0:
        return {}

    false_pass_list = false_pass_list or []
    false_fail_list = false_fail_list or []

    passed_count = sum(1 for r in results if r.get("validation_status") == "PASS")
    failed_count = sum(1 for r in results if r.get("validation_status") == "FAIL")
    fallback_count = sum(1 for r in results if r.get("fallback") is True)
    
    false_pass_count = len(false_pass_list)
    false_fail_count = len(false_fail_list)

    total_orig_tokens = sum(r.get("original_tokens", 0) for r in results)
    total_direct_tokens = sum(r.get("direct_llmlingua_tokens", 0) for r in results)
    total_opt_tokens = sum(r.get("optimized_tokens", 0) for r in results)
    
    macro_average_reduction = sum(r.get("token_reduction_percent", 0.0) for r in results) / total_prompts
    corpus_weighted_reduction = ((total_orig_tokens - total_opt_tokens) / max(1, total_orig_tokens)) * 100.0

    token_reductions = [r.get("token_reduction_percent", 0.0) for r in results]
    direct_reductions = [r.get("direct_reduction_percent", 0.0) for r in results]
    retention_rates = [r.get("retention_rate", 1.0) for r in results]
    
    # Model calls per prompt
    model_calls_list = [r.get("llmlingua_calls", r.get("retries", 1)) for r in results]
    
    # Latencies
    total_latencies = [r.get("total_time_ms", 0.0) for r in results]
    compress_latencies = [r.get("compression_time_ms", 0.0) for r in results]
    val_latencies = [r.get("validation_time_ms", 0.0) for r in results]
    protect_latencies = [r.get("protection_time_ms", 0.0) for r in results]

    # Latency by model call count
    latency_by_calls_map: Dict[int, List[float]] = {}
    for r in results:
        calls = r.get("llmlingua_calls", 1)
        lat = r.get("total_time_ms", 0.0)
        latency_by_calls_map.setdefault(calls, []).append(lat)

    latency_by_calls_summary = {}
    for calls, lats in sorted(latency_by_calls_map.items()):
        latency_by_calls_summary[f"{calls}_call_ms"] = {
            "prompt_count": len(lats),
            "mean_ms": round(sum(lats) / len(lats), 2),
            "median_ms": round(percentile(lats, 50), 2),
            "p95_ms": round(percentile(lats, 95), 2)
        }

    # Category breakdown
    category_map: Dict[str, List[Dict[str, Any]]] = {}
    for r in results:
        cat = r.get("category", "unknown")
        category_map.setdefault(cat, []).append(r)

    category_breakdown = {}
    for cat, items in category_map.items():
        cat_count = len(items)
        cat_reductions = [i.get("token_reduction_percent", 0.0) for i in items]
        cat_direct_reductions = [i.get("direct_reduction_percent", 0.0) for i in items]
        cat_fails = sum(1 for i in items if i.get("validation_status") == "FAIL")
        cat_fallbacks = sum(1 for i in items if i.get("fallback") is True)
        cat_latencies = [i.get("total_time_ms", 0.0) for i in items]
        cat_calls = [i.get("llmlingua_calls", 1) for i in items]

        cat_fp = sum(1 for fp in false_pass_list if fp.get("category") == cat)
        cat_ff = sum(1 for ff in false_fail_list if ff.get("category") == cat)

        category_breakdown[cat] = {
            "prompt_count": cat_count,
            "average_reduction_percent": round(sum(cat_reductions) / cat_count, 2) if cat_count else 0.0,
            "median_reduction_percent": round(percentile(cat_reductions, 50), 2),
            "direct_llmlingua_avg_reduction_percent": round(sum(cat_direct_reductions) / cat_count, 2) if cat_count else 0.0,
            "validation_failures": cat_fails,
            "fallbacks": cat_fallbacks,
            "false_passes": cat_fp,
            "false_fails": cat_ff,
            "average_latency_ms": round(sum(cat_latencies) / cat_count, 2) if cat_count else 0.0,
            "average_model_calls": round(sum(cat_calls) / cat_count, 2) if cat_count else 0.0
        }

    return {
        "dataset_total_prompts": total_prompts,
        "passed": passed_count,
        "failed": failed_count,
        "fallbacks": fallback_count,
        "fallback_rate_percent": round((fallback_count / total_prompts) * 100.0, 2),
        "false_pass_count": false_pass_count,
        "false_pass_rate_percent": round((false_pass_count / max(1, len([r for r in results if r.get("category") == "adversarial"]))) * 100.0, 2),
        "false_fail_count": false_fail_count,
        "false_fail_rate_percent": round((false_fail_count / total_prompts) * 100.0, 2),
        "validation_failure_rate_percent": round((failed_count / total_prompts) * 100.0, 2),
        
        "total_original_tokens": total_orig_tokens,
        "total_direct_llmlingua_tokens": total_direct_tokens,
        "total_optimized_tokens": total_opt_tokens,
        "total_tokens_saved": total_orig_tokens - total_opt_tokens,
        
        "macro_average_reduction_percent": round(macro_average_reduction, 2),
        "corpus_weighted_reduction_percent": round(corpus_weighted_reduction, 2),

        "direct_llmlingua": {
            "average_reduction_percent": round(sum(direct_reductions) / total_prompts, 2),
            "median_reduction_percent": round(percentile(direct_reductions, 50), 2)
        },
        
        "shrinktoken_pro": {
            "average_token_reduction_percent": round(macro_average_reduction, 2),
            "corpus_weighted_reduction_percent": round(corpus_weighted_reduction, 2),
            "median_token_reduction_percent": round(percentile(token_reductions, 50), 2),
            "token_reduction_distribution": {
                "min": round(min(token_reductions), 2) if token_reductions else 0.0,
                "p25": round(percentile(token_reductions, 25), 2),
                "median_p50": round(percentile(token_reductions, 50), 2),
                "p75": round(percentile(token_reductions, 75), 2),
                "p95": round(percentile(token_reductions, 95), 2),
                "max": round(max(token_reductions), 2) if token_reductions else 0.0,
                "mean": round(macro_average_reduction, 2)
            },
            "retention_rate_distribution": {
                "min": round(min(retention_rates), 4) if retention_rates else 1.0,
                "p25": round(percentile(retention_rates, 25), 4),
                "median_p50": round(percentile(retention_rates, 50), 4),
                "p75": round(percentile(retention_rates, 75), 4),
                "p95": round(percentile(retention_rates, 95), 4),
                "max": round(max(retention_rates), 4) if retention_rates else 1.0,
                "mean": round(sum(retention_rates) / total_prompts, 4)
            }
        },
        
        "latency_ms": {
            "total_latency": {
                "mean": round(sum(total_latencies) / total_prompts, 2),
                "median": round(percentile(total_latencies, 50), 2),
                "p95": round(percentile(total_latencies, 95), 2)
            },
            "compression_latency": {
                "mean": round(sum(compress_latencies) / total_prompts, 2),
                "median": round(percentile(compress_latencies, 50), 2),
                "p95": round(percentile(compress_latencies, 95), 2)
            },
            "validation_latency": {
                "mean": round(sum(val_latencies) / total_prompts, 2),
                "median": round(percentile(val_latencies, 50), 2),
                "p95": round(percentile(val_latencies, 95), 2)
            },
            "protection_latency": {
                "mean": round(sum(protect_latencies) / total_prompts, 2),
                "median": round(percentile(protect_latencies, 50), 2),
                "p95": round(percentile(protect_latencies, 95), 2)
            },
            "by_model_calls": latency_by_calls_summary
        },
        
        "model_calls_distribution": {
            "mean": round(sum(model_calls_list) / total_prompts, 2),
            "median": round(percentile(model_calls_list, 50), 2),
            "p95": round(percentile(model_calls_list, 95), 2),
            "max": max(model_calls_list) if model_calls_list else 0
        },
        
        "hypothetical_cost_model_usd": {
            "note": "Hypothetical cost savings based on benchmark token reduction at $2.50 per 1M input tokens (GPT-4o benchmark rate). Not actual claimed dollar savings.",
            "price_per_1m_input_tokens_usd": 2.50,
            "original_inference_cost_usd": round((total_orig_tokens / 1000000.0) * 2.50, 6),
            "optimized_inference_cost_usd": round((total_opt_tokens / 1000000.0) * 2.50, 6),
            "gross_token_savings_usd": round(((total_orig_tokens - total_opt_tokens) / 1000000.0) * 2.50, 6)
        },
        
        "false_passes": false_pass_list,
        "false_failures": false_fail_list,
        "category_breakdown": category_breakdown
    }
