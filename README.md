# ShrinkToken Pro ⚡

**Instruction-Preserving Prompt Optimization & Safety Middleware for LLM APIs**

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![LLMLingua-2](https://img.shields.io/badge/compression-LLMLingua--2-orange.svg)](https://github.com/microsoft/LLMLingua)
[![Tests](https://img.shields.io/badge/tests-105%20passed-brightgreen.svg)]()
[![False Pass Rate](https://img.shields.io/badge/false__pass__rate-~0.00%25-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview & Design Philosophy

Raw statistical prompt compression models (such as unvalidated `LLMLingua-2`) trim subword tokens based on statistical importance probabilities. In complex enterprise workflows, unvalidated statistical compression can lead to instruction loss:
- **Negation Polarity Flips:** *"Do not ask for user credentials"* $\rightarrow$ *"Ask for user credentials"*
- **Numeric & Scale Alterations:** *"Limit payload size to 10 MB"* $\rightarrow$ *"Limit payload size to 100 MB"*
- **Format Distortions:** *"Return only a single floating point number"* $\rightarrow$ *"Return a multi-paragraph explanation"*
- **Path & Target Shifts:** `C:\Users\ASUS\.gemini\config.json` $\rightarrow$ `C:\Windows\System32\cmd.exe`

**ShrinkToken Pro** acts as a safety middleware. It evaluates compressed candidates through a multi-layer deterministic validation engine (`NegationValidator`, `NumericValidator`, `StructuralValidator`, `FormatValidator`, `AudienceValidator`). If a compressed candidate fails validation, the system falls back to the original prompt verbatim (`fallback_text == original_text`).

> *Note: Compression is optional; safety and correctness are prioritized over aggressive token reduction. If a prompt cannot be safely compressed, it is returned unchanged.*

---

## ⚙️ Architecture Pipeline

```
[ Incoming Prompt ]
        │
        ▼
[ Tier 1: CompressibilityAnalyzer ] ─── (Short/Code/JSON) ───► [ Return Original Prompt ]
        │ (Compressible)                                        (Calls = 0, Time ~0.05ms)
        ▼
[ Tier 2: ProtectionEngine ] ───────► Protect Code, JSON, URLs with Syntax Placeholders
        │
        ▼
[ Tier 3: AdaptiveCompressor ] ──────► LLMLingua-2 Importance Scoring (Max 4 Calls Cap)
        │
        ▼
[ Tier 4: ConstraintValidator ] ─────► Negation, Numeric, Format, Structural, Audience
        │
    ┌───┴───────────────┐
 (VALID)            (INVALID)
    │                   │
    v                   v
[ Return Compressed ] [ Tier 5: Strict Fallback to Verbatim Original Prompt ]
```

---

## 📊 Empirical Benchmark Summary (405 Prompts)

Below are approximate empirical results collected on a benchmark dataset of 405 prompts across 13 categories (general, multi-constraint, reasoning, RAG, agents, code, JSON, negations, numeric constraints, output formats, ranges, roles, URLs/paths, and adversarial prompts).

*Disclaimer: Figures are approximate benchmark measurements on CPU hardware. Token savings and latency vary depending on hardware acceleration (CUDA vs CPU), prompt category, and constraint density.*

| Benchmark Metric | Direct LLMLingua-2 | ShrinkToken Pro (Empirical Benchmark) |
|---|---|---|
| **Evaluated Prompts** | 405 | **405 prompts** |
| **False-Pass Rate (Unsafe Accepts)** | ~34.00% | **~0.00%** (0/50 accepted on adversarial set) |
| **False-Fail Rate (Unsafe Rejects)** | 0.00% | **~0.00%** (0/355 rejected on safe set) |
| **Fallback Rate** | 0.00% | **~5.68%** (23 fallbacks on high-risk prompts) |
| **Corpus Subword Token Reduction** | ~34.50% | **~3.33%** (~308 subword tokens saved) |
| **Macro Average Reduction** | ~34.50% | **~2.07%** |
| **Mean Model Calls / Prompt** | 1.00 call | **~0.67 calls** (via early exit filtering) |
| **Max Model Call Limit** | Uncapped | **4 calls MAX** (Authoritative cap) |
| **Mean Total Latency (CPU)** | ~1400 ms | **~2106 ms** |
| **P95 Latency (CPU)** | ~8600 ms | **~6278 ms** |

### Category Breakdown (Approximate)
- **Compressible Prose Categories:** `general` (~10.6% reduction), `multi_constraint` (~9.4% reduction), `reasoning` (~8.6% reduction), `agents` (~2.7% reduction), `rag` (~2.5% reduction).
- **Protected / Non-Prose Categories:** `code`, `json`, `negation`, `numeric_constraints`, `output_formats`, `ranges`, `roles`, `urls_paths`, `adversarial` (~0.00% reduction via early exit protection).

---

## 🛠️ Quick Start

### 1. Installation & Environment
```bash
# Clone repository
git clone https://github.com/AREKG0/shrinktoken.git
cd shrinktoken

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Run Test Suite
```bash
$env:PYTHONPATH="."; pytest backend/tests/ -m "not slow" -v
```

### 3. Run Benchmark Suite & Integrity Audit
```bash
$env:PYTHONPATH="."; python backend/benchmarks/runner.py
```

### 4. Basic Code Usage
```python
from backend.app.compression.llmlingua import LLMLinguaCompressor
from backend.app.services.compression_engine import CompressionService
from backend.app.models.prompt import CompressionMode

# Initialize compressor and service
compressor = LLMLinguaCompressor()
service = CompressionService(compressor)

prompt = "Explain quantum computing to a beginner using simple analogies."
result, telemetry = service.optimize_with_telemetry(prompt, mode=CompressionMode.balanced)

print(f"Original Tokens: {result.original_tokens}")
print(f"Compressed Tokens: {result.compressed_tokens}")
print(f"Optimized Text: {result.compressed_text}")
print(f"Fallback Triggered: {telemetry.fallback}")
```

---

## 📁 Repository Map

```
shrinktoken/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (/v1/optimize, /v1/validate, /v1/cost)
│   │   ├── compression/  # LLMLinguaCompressor, AdaptiveCompressor, CompressibilityAnalyzer
│   │   ├── core/         # Config (MAX_MODEL_CALLS=4), Logging, Exceptions
│   │   ├── models/       # Pydantic schemas (Prompt, CompressionResult, Telemetry)
│   │   ├── services/     # CompressionService, RAGStrategy, CostEngine
│   │   └── validators/   # ConstraintValidator, FormatValidator, AudienceValidator, NegationValidator
│   ├── benchmarks/       # 405 benchmark prompts, runner.py, integrity_checker.py, reporter.py
│   └── tests/            # 105 unit & integration tests
├── ARCHITECTURE_AND_GOALS.md  # Detailed architecture specifications
├── PHASE_6_75_REPORT.md      # Empirical benchmark audit report
└── PROJECT_COMPLETE_SUMMARY.md # Master project summary chronicle
```

---

## 📜 License

Distributed under the **MIT License**. Uses Microsoft `LLMLingua-2`.
