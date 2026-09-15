# ShrinkToken Pro — Architecture

## System Overview

ShrinkToken Pro is an instruction-preserving prompt optimization engine. It reduces LLM API input token costs while maintaining the behavioral fidelity of the original prompt.

## Pipeline

```
USER INPUT
    ↓
┌─────────────────────────┐
│    Prompt Parser         │ → Identifies: Role, Task, Instructions, Constraints,
│                          │   Examples, Context, Questions, Output Requirements
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Critical Instruction     │ → Extracts hard constraints, negations, numbers,
│ Extractor                │   code blocks, URLs, JSON, exact formats
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Protected Content Layer  │ → Marks segments that MUST NOT be modified
│                          │   during compression
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Compression Engine       │ → LLMLingua-2 (baseline) or custom model
│                          │   Modes: SAFE / BALANCED / AGGRESSIVE
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Validation Layer         │
│  ├─ Constraint Validator │ → Checks all hard constraints preserved
│  ├─ Negation Validator   │ → Ensures logical polarity unchanged
│  ├─ Numeric Validator    │ → Verifies numbers, ranges, dates intact
│  ├─ Format Validator     │ → Checks JSON, code, URLs preserved
│  ├─ Semantic Validator   │ → Embedding similarity score
│  └─ Behavioral Validator │ → Optional: compares LLM outputs
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Cost/Latency Calculator  │ → Net savings = original - optimized - overhead
└─────────────────────────┘
    ↓
SAFE OPTIMIZED PROMPT (or fallback to original)
```

## Adaptive Compression Strategy

The system does not blindly compress to a target percentage. Instead:

1. Attempt target compression
2. Validate result
3. If validation PASSES → try stronger compression
4. If validation FAILS → reduce compression
5. Binary search until maximum safe compression found

```
50% → FAIL
40% → FAIL
30% → PASS
35% → PASS
37% → FAIL
35% → FINAL (maximum safe compression = 35%)
```

## Compression Engine Abstraction

All compressors implement `BaseCompressor`:

```python
class BaseCompressor(ABC):
    @abstractmethod
    def compress(self, text: str, config: CompressionConfig) -> CompressionResult:
        ...
```

Current implementations:
- `LLMLinguaCompressor` — Microsoft LLMLingua-2 (XLM-RoBERTa-large)
- `RuleBasedCompressor` — Planned
- `AdaptiveCompressor` — Planned (wraps any compressor with binary search)

## Technology Decisions

| Decision | Rationale |
|----------|-----------|
| LLMLingua-2 as baseline | Proven compression, no custom training needed initially |
| Abstract compressor interface | Allows future model swap without rewriting the pipeline |
| Pydantic models | Type safety, validation, serialization for API |
| FastAPI | Async-capable, auto-docs, production-ready |
| SQLite → PostgreSQL | Start simple, scale when needed |
| CPU-only initially | User hardware constraint; LLMLingua-2 encoder models run fine on CPU |
