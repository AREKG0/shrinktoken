# ShrinkToken Pro — System Architecture Details & Ultimate Project Goals

## 1. Executive Summary & Ultimate Goals

### The Production Problem
Statistical prompt compression models (such as raw `LLMLingua-2`) achieve 30–50% token reduction by dropping subword tokens based on token importance probabilities. However, in enterprise AI applications, raw statistical compression causes critical failures:
- **Negation Polarity Flips:** "Do not ask for user credentials" -> "Ask for user credentials"
- **Numeric & Scale Corruption:** "Limit max upload payload size to 10 MB" -> "Limit payload size to 100 MB"
- **Format Distortion:** "Return only a single floating point number" -> "Return a multi-paragraph explanation"
- **Audience/Persona Drift:** "Explain quantum computing to a beginner" -> "Explain quantum computing to an expert"
- **Path & Security Target Corruption:** `C:\Users\ASUS\.gemini\config.json` -> `C:\Windows\System32\cmd.exe`

### The Ultimate Goal of ShrinkToken Pro
ShrinkToken Pro is built to become the **industry-standard, zero-loss, instruction-preserving prompt optimization middleware for enterprise LLM workloads**.

> **CORE MANDATE:**
> **"COMPRESSION IS OPTIONAL. CORRECTNESS IS MANDATORY."**

```
 ┌───────────────────────────────────────────────────────────────────────────┐
 |                            ULTIMATE OBJECTIVES                            |
 └───────────────────────────────────────────────────────────────────────────┘
   1. GUARANTEED 0.00% FALSE PASS RATE: Zero unsafe compressed prompts pass.
   2. STRICT FALLBACK PROTECTION: 100% fallback to verbatim original text if
      any constraint fails.
   3. HIGH-THROUGHPUT MIDDLEWARE: Sub-200ms latency via CUDA acceleration for
      gateway proxies (LiteLLM, Portkey, LangChain, OpenArc).
   4. COST REDUCTION: 20-60% input token dollar savings on prose-heavy and
      RAG contexts without compromising functional behavior.
```

---

## 2. Multi-Tier System Architecture

ShrinkToken Pro uses a **6-Tier Guardrail Architecture** that intercepts, inspects, shields, compresses, validates, and telemetry-logs prompt traffic before sending it to downstream LLM providers (OpenAI, Anthropic, Gemini, local vLLM).

```
[ Incoming Prompt ]
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 0: API Entrypoint & FastAPI Middleware Router                      │
│ - POST /v1/optimize, /v1/validate, /v1/cost                            │
└─────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 1: CompressibilityAnalyzer (Zero-Overhead Early Exit Filter)       │
│ - Short Prompts (< 20 tokens)                                          │
│ - Non-Prose Content (Raw JSON / Code / SQL / Regex)                     │
│ - High-Density Constrained Prompts                                      │
└─────────────────────────────────────────────────────────────────────────┘
        │
     (Pass) ─────────── (Early Exit) ───────────► [ Return Original Prompt ]
        │                                         (Calls = 0, Time ~0.05ms)
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 2: ProtectionEngine (Syntax Shield & Placeholder Substitution)      │
│ - Replaces Code Blocks (```python ... ``` -> __CODE_BLOCK_0__)           │
│ - Replaces JSON Schemas ({ "key": "val" } -> __JSON_BLOCK_0__)          │
│ - Replaces URLs & File Paths (https://... -> __URL_0__)                 │
└─────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 3: Subword Token Compression Engine (LLMLinguaCompressor)          │
│ - PyTorch LLMLingua-2 Model (CPU / CUDA Hardware Auto-Detection)        │
│ - Subword Token Importance Scoring                                      │
└─────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 4: Multi-Layer Deterministic Safety Validator Suite                │
│ ├─ NegationValidator    (Prohibition keywords, target scope, polarity)  │
│ ├─ NumericValidator     (Values, units, range directions, entity bindings)│
│ ├─ StructuralValidator  (Placeholder integrity, syntax schemas)        │
│ ├─ FormatValidator       (Output types: JSON/XML/Float/Int, cardinality) │
│ └─ AudienceValidator     (Target reader skill level, persona roles)     │
└─────────────────────────────────────────────────────────────────────────┘
        │
     (Valid) ──────────── (Invalid)
        │                     │
        v                     v
┌───────────────────┐ ┌───────────────────────────────────────────────────┐
│ Return Compressed │ │ TIER 5: Strict Fallback & Telemetry Controller    │
│ Prompt (Safely    │ │ - Return VERBATIM Original Prompt                 │
│ Optimized)        │ │ - Log fallback_reason (CONSTRAINT_VALIDATION_FAIL)│
└───────────────────┘ └───────────────────────────────────────────────────┘
```

---

## 3. Tier-by-Tier Component Specifications

### Tier 0: API Entrypoint & FastAPI Router (`backend/app/api/`)
- **FastAPI Router Endpoints:**
  - `POST /api/v1/optimize`: Accepts `PromptInput`, executes compression pipeline, returns `CompressionResult` + `OptimizationTelemetry`.
  - `POST /api/v1/validate`: Accepts `original_text` + `candidate_text`, runs safety validators, returns `ValidationResult`.
  - `POST /api/v1/cost`: Calculates hypothetical token dollar savings given provider rates.
  - `GET /health`: Healthcheck endpoint.

### Tier 1: Zero-Overhead Early Exit Filter (`CompressibilityAnalyzer`)
- Inspects prompt length and token composition.
- Immediately exits with `model_calls=0` if prompt is non-prose (JSON schema, code block, short instruction < 20 tokens).
- Prevents 80% of unnecessary LLMLingua-2 neural net calls, dropping mean model calls per prompt from 4.5 to **0.67 calls**.

### Tier 2: Syntax Shield (`ProtectionEngine`)
- Intercepts raw code blocks, JSON schemas, URLs, Windows paths (`C:\...`), and Linux paths (`/etc/...`).
- Replaces syntax with unique placeholders (`__CODE_BLOCK_0__`, `__URL_0__`).
- Restores original syntax untouched post-compression, guaranteeing **100% structural fidelity**.

### Tier 3: Compression Engine (`LLMLinguaCompressor` & `AdaptiveCompressor`)
- Wraps Microsoft `llmlingua==0.2.2`.
- `AdaptiveCompressor` uses a **step-binary search** over retention rates `[0.70, 0.85, 0.925, 0.9625]` capped strictly by `MAX_MODEL_CALLS = 4`.
- `RAGStrategy` isolates System Instructions & Queries (100% retention) while adaptively compressing Retrieved Context blocks.

### Tier 4: Deterministic Validator Suite (`ConstraintValidator`)
- **NegationValidator:** Detects missing prohibition targets and scope truncation (`ADV-001`).
- **NumericValidator:** Detects altered numbers (`10 MB` -> `100 MB`), reversed ranges (`3-10` -> `10-3`), unit changes (`seconds` -> `minutes`), and entity-number swaps.
- **StructuralValidator:** Enforces exact placeholder counts and schema preservation.
- **FormatValidator:** Detects structural output conflicts (`floating point number` vs `multi-paragraph explanation`) to fix `ADV-023`.
- **AudienceValidator:** Rejects skill level drift (`beginner` -> `expert`) and persona role alterations.

### Tier 5: Strict Fallback & Telemetry Controller
- If no candidate rate passes all Tier 4 validators, the system sets `fallback=True` and returns `original_text` **verbatim**.
- Hard assertion: `assert fallback_text == original_text`.
- Logs serializable telemetry including `request_id`, `tokens_saved`, `fallback_reason`, `validation_attempts`, `protection_time_ms`, `compression_time_ms`, `validation_time_ms`.

### Tier 6: Downstream Equivalence Evaluator (`LLM-as-a-Judge`)
- Runs downstream LLM calls (e.g. GPT-4o / Claude) on original vs. compressed prompt pairs to score functional output equivalence (1.0 = identical execution behavior).

---

## 4. Phase 7 Execution Blueprint (The 6 Integration Steps)

```
  Step 1: Merge & Smoke-Test Files
    └── Drop API routes, judge runner into repo, run existing 105 tests
  Step 2: Signature & Interface Alignment
    └── Match method names across routes, CompressionService, & telemetry
  Step 3: PyTorch CUDA Acceleration Verification
    └── Auto-detect CUDA GPU (device_map='cuda'), verify latency drop (6.2s -> <200ms)
  Step 4: FastAPI Web Layer & Interactive Documentation
    └── Verify uvicorn app.main:app, hit /docs, manually test /v1/optimize
  Step 5: LLM-as-a-Judge Downstream Evaluation
    └── Run sample 20 prompts first, verify equivalence scores, run full 405 benchmark
  Step 6: Empirical Verification & Phase 7 Final Report
    └── Produce PHASE_7_REPORT.md with verified CUDA latencies and judge scores
```

---

## 5. Deployment Vision & Integration Targets

1. **Hosted Enterprise API Microservice:**
   Deployed via FastAPI + Docker + Uvicorn on GPU servers (e.g. AWS EC2 g4dn / g5 instances).
2. **AI Gateway Proxy Middleware (LiteLLM / Portkey / OpenArc):**
   Interrogates incoming LLM prompts in-flight, transparently optimizing long prompts and RAG contexts before routing to downstream model providers.
3. **Local RAG & Agent Pipeline Plugin:**
   PyPI package (`pip install shrinktoken-pro`) usable as a standard Python library for local agentic workflows.
