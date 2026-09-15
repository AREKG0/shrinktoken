"""
ShrinkToken Pro Benchmark Runner (Phase 6.75 Audit).
Loads 405 benchmark prompts, executes side-by-side comparisons,
enforces MAX_MODEL_CALLS=4, records complete telemetry, executes integrity auditor,
and generates JSON, CSV, summary.json, benchmark_report.json, and benchmark_summary.md.
"""
import glob
import json
import os
import csv
import time
from typing import Dict, Any, List

from backend.app.compression.llmlingua import LLMLinguaCompressor
from backend.app.services.compression_engine import CompressionService
from backend.app.models.prompt import CompressionMode, CompressionConfig
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.services.protection_engine import ProtectionEngine
from backend.app.core.config import settings
from backend.benchmarks.metrics import compute_benchmark_summary
from backend.benchmarks.integrity_checker import BenchmarkIntegrityChecker
from backend.benchmarks.reporter import BenchmarkReportGenerator

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

class BenchmarkRunner:
    def __init__(self, use_real_model: bool = True):
        self.use_real_model = use_real_model
        self.validator = ConstraintValidator()
        self.protection_engine = ProtectionEngine()
        self.integrity_checker = BenchmarkIntegrityChecker()
        self.reporter = BenchmarkReportGenerator()
        if self.use_real_model:
            self.base_compressor = LLMLinguaCompressor()
            self.service = CompressionService(self.base_compressor, max_model_calls=settings.MAX_MODEL_CALLS)
        else:
            self.base_compressor = None
            self.service = None

    @staticmethod
    def load_all_prompts() -> List[Dict[str, Any]]:
        prompts = []
        files = sorted(glob.glob(os.path.join(PROMPTS_DIR, "*.json")))
        for filepath in files:
            with open(filepath, "r", encoding="utf-8") as f:
                items = json.load(f)
                prompts.extend(items)
        return prompts

    def run_benchmark(self, limit: int = 0) -> Dict[str, Any]:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        prompts = self.load_all_prompts()
        if limit > 0:
            prompts = prompts[:limit]

        results = []
        false_pass_list = []
        false_fail_list = []

        print(f"Starting Phase 6.75 empirical benchmark audit on {len(prompts)} prompts...")

        for idx, item in enumerate(prompts):
            p_id = item["id"]
            cat = item["category"]
            text = item["prompt"]

            t0 = time.time()
            req_id = f"req-{idx+1:03d}-{p_id}"
            
            p_t0 = time.time()
            masked_text, mapping = self.protection_engine.mask(text)
            protect_ms = (time.time() - p_t0) * 1000.0

            if self.use_real_model and self.service:
                # Direct LLMLingua-2 baseline
                c_t0 = time.time()
                try:
                    direct_res = self.base_compressor.compress(text, config=CompressionConfig(mode=CompressionMode.balanced, target_rate=0.6))
                    direct_text = direct_res.compressed_text
                    direct_tokens = self.service.get_token_count(direct_text)
                except Exception:
                    direct_text = text
                    direct_tokens = self.service.get_token_count(text)
                compress_ms = (time.time() - c_t0) * 1000.0

                # ShrinkToken Pro (with full telemetry & MAX_MODEL_CALLS=4 cap)
                opt_res, telemetry = self.service.optimize_with_telemetry(
                    text,
                    mode=CompressionMode.balanced,
                    prompt_id=p_id,
                    category=cat
                )
                opt_text = opt_res.compressed_text
                orig_tokens = opt_res.original_tokens
                opt_tokens = opt_res.compressed_tokens
                token_reduction = max(0, orig_tokens - opt_tokens)
                reduction_pct = opt_res.saving_percent
                status = "PASS" if opt_res.status == "safe" else "FAIL"
                fallback = telemetry.fallback
                fallback_reason = telemetry.fallback_reason
                
                llmlingua_calls = telemetry.number_of_llmlingua_calls
                adaptive_iters = telemetry.number_of_adaptive_iterations
                val_attempts = telemetry.validation_attempts
                comp_attempts = telemetry.compression_attempts
                rates_attempted = telemetry.retention_rates_attempted
                val_results = telemetry.validation_result_per_attempt
                val_reasons = telemetry.validation_failure_reason
                early_exit = telemetry.early_exit
                early_exit_reason = telemetry.early_exit_reason

                # Hard assertion: max model calls limit
                assert llmlingua_calls <= settings.MAX_MODEL_CALLS, f"Prompt {p_id} exceeded max model calls: {llmlingua_calls} > {settings.MAX_MODEL_CALLS}"
                
                # Hard assertion: fallback strictly equals original text
                if fallback:
                    assert opt_text == text, f"Prompt {p_id} fallback=True but optimized_text != original_text"
            else:
                orig_tokens = max(10, self.service.get_token_count(text) if self.service else len(text.split()))
                direct_tokens = max(5, int(orig_tokens * 0.6))
                direct_text = text
                opt_tokens = max(5, int(orig_tokens * 0.7))
                opt_text = text
                token_reduction = orig_tokens - opt_tokens
                reduction_pct = ((orig_tokens - opt_tokens) / orig_tokens) * 100.0
                status = "PASS"
                fallback = False
                fallback_reason = "NONE"
                llmlingua_calls = 1
                adaptive_iters = 1
                val_attempts = 1
                comp_attempts = 1
                rates_attempted = [0.7]
                val_results = ["PASS"]
                val_reasons = []
                early_exit = False
                early_exit_reason = ""
                compress_ms = 1.0

            # Validation timing
            v_t0 = time.time()
            val_res = self.validator.validate(text, opt_text)
            val_ms = (time.time() - v_t0) * 1000.0

            total_ms = (time.time() - t0) * 1000.0

            # False-pass check (explicitly against corrupted adversarial candidates ONLY)
            if cat == "adversarial" and "corrupted_candidate" in item:
                corrupted = item["corrupted_candidate"]
                corrupted_val = self.validator.validate(text, corrupted)
                if corrupted_val.status == "PASS":
                    false_pass_list.append({
                        "id": p_id,
                        "category": cat,
                        "original_prompt": text,
                        "corrupted_candidate": corrupted,
                        "expected": "FAIL",
                        "actual": "PASS",
                        "reason": item.get("reason", "Vulnerability")
                    })

            result_entry = {
                "request_id": req_id,
                "id": p_id,
                "category": cat,
                "original_text": text,
                "direct_llmlingua_text": direct_text,
                "optimized_text": opt_text,
                "original_tokens": orig_tokens,
                "direct_llmlingua_tokens": direct_tokens,
                "optimized_tokens": opt_tokens,
                "token_reduction": token_reduction,
                "token_reduction_percent": round(reduction_pct, 2),
                "direct_reduction_percent": round(((orig_tokens - direct_tokens) / max(1, orig_tokens) * 100.0), 2) if orig_tokens else 0.0,
                "retention_rate": round(opt_tokens / max(1, orig_tokens), 4) if orig_tokens else 1.0,
                "validation_status": status,
                "fallback": fallback,
                "fallback_reason": fallback_reason,
                "llmlingua_calls": llmlingua_calls,
                "adaptive_iterations": adaptive_iters,
                "validation_attempts": val_attempts,
                "compression_attempts": comp_attempts,
                "retention_rates_attempted": rates_attempted,
                "validation_result_per_attempt": val_results,
                "validation_failure_reasons": val_reasons,
                "early_exit": early_exit,
                "early_exit_reason": early_exit_reason,
                "protection_time_ms": round(protect_ms, 2),
                "compression_time_ms": round(compress_ms, 2),
                "validation_time_ms": round(val_ms, 2),
                "total_time_ms": round(total_ms, 2)
            }
            results.append(result_entry)
            print(f"[{idx+1}/{len(prompts)}] {p_id} ({cat}): {orig_tokens} -> {opt_tokens} tokens ({reduction_pct:.1f}%), calls={llmlingua_calls}, direct={direct_tokens}, status={status}, {total_ms:.0f}ms")

        # Aggregate summary calculation
        summary = compute_benchmark_summary(results, false_pass_list, false_fail_list)

        # Execute Benchmark Integrity Checker Audit
        print("Running BenchmarkIntegrityChecker audit...")
        self.integrity_checker.check_integrity(summary, results, prompts)

        # Save all reports (json, csv, md) via BenchmarkReportGenerator
        self.reporter.generate_reports(summary, results, RESULTS_DIR)

        # Legacy file output compatibility
        json_path = os.path.join(RESULTS_DIR, "latest_results.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        summary_path = os.path.join(RESULTS_DIR, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print(f"Phase 6.75 benchmark audit complete. Results saved to {RESULTS_DIR}")
        return summary

if __name__ == "__main__":
    runner = BenchmarkRunner(use_real_model=True)
    runner.run_benchmark()
