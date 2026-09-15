# ShrinkToken Pro — Phase 6.75 Benchmark Audit Summary

## 1. Executive Summary
- **Dataset Size:** 405 benchmark prompts across 14 categories
- **Macro Average Token Reduction:** 2.07%
- **Corpus-Weighted Token Reduction:** 3.33% (308 tokens saved out of 9,243 total tokens)
- **Tokenization Methodology:** Single authoritative tokenizer (`microsoft/llmlingua-2-xlm-roberta-large-meetingbank`)
- **Hardware & PyTorch Device:** CPU (`device_map='cpu'`)

## 2. Safety & Validation Audit
- **Passed Benchmark Validation:** 382 / 405 (94.32%)
- **Validation Failures:** 23 (5.68%)
- **Fallback Rate:** 5.68% (23 prompts)
- **False-Pass Rate:** 0.00% (0 / 50 adversarial prompts)
- **False-Fail Rate:** 0.00% (0 false rejections)

## 3. Telemetry & Model Call Limits
- **MAX_MODEL_CALLS Cap:** 4 calls (strictly enforced)
- **Mean Model Calls / Prompt:** 0.67 calls
- **Median Model Calls:** 0.00 calls
- **P95 Model Calls:** 4.00 calls
- **Max Model Calls Observed:** 4 calls

## 4. Latency Distribution (ms)
- **Mean Total Latency:** 2106.70 ms
- **Median Total Latency:** 1249.58 ms
- **P95 Total Latency:** 6278.72 ms
- **Compression Time (Mean):** 1269.57 ms
- **Validation Time (Mean):** 0.41 ms
- **Protection Time (Mean):** 0.05 ms

### Latency by Model Call Count:
- **0_call_ms:** 336 prompts | Mean: 1274.18 ms | Median: 1240.52 ms | P95: 1316.58 ms
- **1_call_ms:** 1 prompts | Mean: 2487.21 ms | Median: 2487.21 ms | P95: 2487.21 ms
- **3_call_ms:** 2 prompts | Mean: 5134.29 ms | Median: 5134.29 ms | P95: 5276.26 ms
- **4_call_ms:** 66 prompts | Mean: 6247.48 ms | Median: 6220.57 ms | P95: 6473.22 ms

## 5. Category Breakdown Performance
| Category | Prompt Count | Macro Avg % | Direct LLMLingua Avg % | Fallbacks | False Passes | False Fails | Mean Calls | Mean Latency (ms) |
|---|---|---|---|---|---|---|---|---|
| adversarial | 50 | 0.00% | 37.78% | 0 | 0 | 0 | 0.00 | 1418.60 ms |
| agents | 15 | 2.73% | 31.94% | 0 | 0 | 0 | 0.53 | 1913.26 ms |
| code | 20 | 0.00% | 41.34% | 0 | 0 | 0 | 0.00 | 1232.36 ms |
| general | 15 | 10.65% | 35.68% | 0 | 0 | 0 | 0.80 | 2239.62 ms |
| json | 20 | 0.00% | 41.46% | 0 | 0 | 0 | 0.00 | 1230.60 ms |
| multi_constraint | 50 | 9.36% | 10.73% | 17 | 0 | 0 | 4.00 | 6225.57 ms |
| negation | 50 | 0.00% | 37.17% | 0 | 0 | 0 | 0.00 | 1211.41 ms |
| numeric_constraints | 50 | 0.00% | 38.65% | 0 | 0 | 0 | 0.00 | 1246.69 ms |
| output_formats | 50 | 0.00% | 37.98% | 0 | 0 | 0 | 0.00 | 1247.34 ms |
| rag | 15 | 2.55% | 36.23% | 5 | 0 | 0 | 2.07 | 3859.32 ms |
| ranges | 25 | 0.00% | 37.26% | 0 | 0 | 0 | 0.00 | 1306.39 ms |
| reasoning | 15 | 8.64% | 33.17% | 1 | 0 | 0 | 1.33 | 3016.37 ms |
| roles | 15 | 0.00% | 39.19% | 0 | 0 | 0 | 0.00 | 1284.85 ms |
| urls_paths | 15 | 0.00% | 41.69% | 0 | 0 | 0 | 0.00 | 1274.30 ms |

## 6. Configurable Cost Model (Hypothetical cost savings based on benchmark token reduction at $2.50 per 1M input tokens (GPT-4o benchmark rate). Not actual claimed dollar savings.)
- **Input Price per 1M Tokens:** $2.50
- **Baseline Cost:** $0.023107
- **Optimized Cost:** $0.022337
- **Gross Token Savings:** $0.000770

## 7. Known Performance Bottlenecks & Limitations
- **CPU Inference Overhead:** Model inference dominates ~95% of execution time on multi-call prompts (~1.3s per CPU pass).
- **GPU Acceleration Required:** Hardware GPU acceleration (`device_map='cuda'`) is recommended for Phase 7 to achieve sub-second execution on multi-constraint prompts.
