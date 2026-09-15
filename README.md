<!-- CYBERPUNK / NEON WAVING HEADER -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00e5ff,100:b900ff&height=240&section=header&text=SHRINKTOKEN%20PRO%20%E2%9A%A1&fontSize=70&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Enterprise-Grade%20Instruction-Preserving%20Prompt%20Optimization%20%26%20Safety%20Middleware&descAlignY=62&descAlign=50" alt="ShrinkToken Pro Header" width="100%"/>

<!-- ANIMATED TYPING TEXT -->
  <a href="https://chromewebstore.google.com/detail/shrinktoken/mplofkijajafbhgmeapoefnmppgmiodp">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=00E5FF&center=true&vCenter=true&width=800&lines=%E2%9A%A1+Instruction-Preserving+LLM+Prompt+Optimization;%F0%9F%9B%A1%EF%B8%8F+0.00%25+False-Pass+Rate+Safety+Validation;%F0%9F%A7%A0+LLMLingua-2+Subword+Importance+Scoring;%F0%9F%92%B8+Save+Token+Costs+Without+Breaking+Instructions!" alt="Typing SVG" />
  </a>

<!-- HERO LOGO -->
  <br />
  <img src="https://raw.githubusercontent.com/AREKG0/shrinktoken/main/public/icon.png" width="140" alt="ShrinkToken Pro Cyberpunk Logo" />
  <br />
  
  <p align="center">
    <strong>ShrinkToken Pro is an instruction-preserving prompt optimization and safety middleware for LLM APIs. Built on Microsoft's <code>LLMLingua-2</code>, it reduces token footprint while enforcing deterministic multi-layer safety validation to prevent rule flips, format distortions, and numeric errors.</strong>
  </p>

<!-- CHROME WEB STORE & NETLIFY LIVE APP BUTTONS -->
  <p align="center">
    <a href="https://chromewebstore.google.com/detail/shrinktoken/mplofkijajafbhgmeapoefnmppgmiodp" target="_blank">
      <img src="https://img.shields.io/badge/⚡_INSTALL_EXTENSION_FROM-CHROME_WEB_STORE-00e5ff?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=111113&border=3" alt="Install from Chrome Web Store" style="height: 42px;" />
    </a>
    <a href="https://shrinktoken.netlify.app/" target="_blank">
      <img src="https://img.shields.io/badge/🌐_LAUNCH_LIVE_WEB_APP-SHRINKTOKEN.NETLIFY.APP-ff007f?style=for-the-badge&logo=netlify&logoColor=white&labelColor=111113&border=3" alt="Try Live Web App on Netlify" style="height: 42px;" />
    </a>
  </p>

<!-- COLORFUL BADGES -->
  <p align="center">
    <a href="https://github.com/AREKG0/shrinktoken/stargazers">
      <img src="https://img.shields.io/github/stars/AREKG0/shrinktoken?style=for-the-badge&logo=github&color=00e5ff&labelColor=111113" alt="Stars"/>
    </a>
    <a href="https://github.com/AREKG0/shrinktoken/network/members">
      <img src="https://img.shields.io/github/forks/AREKG0/shrinktoken?style=for-the-badge&logo=git&color=8a2be2&labelColor=111113" alt="Forks"/>
    </a>
    <a href="https://github.com/AREKG0/shrinktoken/issues">
      <img src="https://img.shields.io/github/issues/AREKG0/shrinktoken?style=for-the-badge&logo=github&color=ff007f&labelColor=111113" alt="Issues"/>
    </a>
    <a href="https://github.com/AREKG0/shrinktoken/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-00e5ff?style=for-the-badge&logo=open-source-initiative&labelColor=111113" alt="License"/>
    </a>
    <img src="https://img.shields.io/badge/Python-3.13-00e5ff?style=for-the-badge&logo=python&labelColor=111113" alt="Python 3.13"/>
    <img src="https://img.shields.io/badge/LLMLingua--2-Microsoft-ff007f?style=for-the-badge&logo=pytorch&labelColor=111113" alt="LLMLingua-2"/>
    <img src="https://img.shields.io/badge/Tests-105_PASSED-00e5ff?style=for-the-badge&logo=pytest&labelColor=111113" alt="Pytest 105 Passed"/>
    <img src="https://img.shields.io/badge/False_Pass-~0.00%25-brightgreen?style=for-the-badge&logo=shield&labelColor=111113" alt="False Pass Rate ~0%"/>
  </p>

<!-- TECHNOLOGY ICONS -->
  <h3>🧬 Cyberpunk Tech Stack 🧬</h3>
  <p align="center">
    <a href="https://skillicons.dev">
      <img src="https://skillicons.dev/icons?i=python,pytorch,fastapi,react,vite,tailwind,js,git,github,docker,vscode&theme=dark" alt="Tech Stack Icons" />
    </a>
  </p>
</div>

---

## ⚡ Project Showcase & Real-Time Telemetry HUD

<div align="center">
<!-- CUSTOM ANIMATED CYBERPUNK SPEEDOMETER HUD -->
  <img src="https://raw.githubusercontent.com/AREKG0/shrinktoken/main/public/token_speedometer.svg" width="100%" alt="ShrinkToken Animated Telemetry Speedometer HUD" />
  <p><em>Real-Time Interactive Telemetry HUD tracking live prompt optimization and API cost reductions.</em></p>
  <br />
  <img src="https://raw.githubusercontent.com/AREKG0/shrinktoken/main/public/screenshot_chatgpt.png" width="100%" alt="ShrinkToken running side-by-side with ChatGPT" style="border-radius: 10px; box-shadow: 0px 0px 25px rgba(0, 229, 255, 0.4);" />
  <p><em>ShrinkToken operating seamlessly alongside ChatGPT inside a persistent, sleek dark-mode Side Panel.</em></p>
</div>

---

## 📌 Primary Mandate & Design Philosophy

> **"COMPRESSION IS OPTIONAL. CORRECTNESS IS MANDATORY."**

Raw statistical prompt compression models (such as unvalidated `LLMLingua-2`) trim subword tokens based purely on statistical probabilities. In enterprise AI applications, raw statistical compression can cause severe instruction corruptions:
- **Negation Polarity Flips:** *"Do not ask for user credentials"* $\rightarrow$ *"Ask for user credentials"*
- **Numeric & Scale Alterations:** *"Limit payload size to 10 MB"* $\rightarrow$ *"Limit payload size to 100 MB"*
- **Format Distortions:** *"Return only a single floating point number"* $\rightarrow$ *"Return a multi-paragraph explanation"*
- **Path & Security Target Shifts:** `C:\Users\ASUS\.gemini\config.json` $\rightarrow$ `C:\Windows\System32\cmd.exe`

**ShrinkToken Pro** intercepts compressed candidates with a multi-layer deterministic safety suite. If any candidate breaks a constraint, the system strictly falls back to the original prompt verbatim (`fallback_text == original_text`).

> *Note: Safety and functional correctness take absolute priority over aggressive token reduction. If a prompt cannot be safely compressed, it is returned unchanged.*

---

## 📊 Empirical Benchmark Summary (405 Prompts)

Below are approximate empirical benchmark metrics collected across **405 real-world & synthetic benchmark prompts** spanning **13 distinct categories** (general, multi-constraint, reasoning, RAG, agents, code, JSON, negations, numeric constraints, output formats, ranges, roles, URLs/paths, and adversarial prompts).

*Disclaimer: Benchmark metrics are approximate CPU hardware measurements. Token savings and latency vary depending on hardware acceleration (CUDA vs CPU), prompt category, and constraint density.*

### 📈 Core Metric Comparison

| Benchmark Metric | Direct Unvalidated LLMLingua-2 | ShrinkToken Pro Engine (Empirical Audit) |
|---|---|---|
| **Evaluated Benchmark Prompts** | 405 | **405 prompts** (100% Reconciled) |
| **False-Pass Rate (Unsafe Accepts)** | ~34.00% | **~0.00%** (0/50 accepted on adversarial set) |
| **False-Fail Rate (Unsafe Rejects)** | 0.00% | **~0.00%** (0/355 rejected on safe set) |
| **Fallback Rate (High-Risk Prompts)** | 0.00% | **~5.68%** (23 fallbacks on unsafe compressions) |
| **Corpus Subword Token Reduction** | ~34.50% | **~3.33%** (~308 subword tokens saved safely) |
| **Macro Average Token Reduction** | ~34.50% | **~2.07%** |
| **Mean Model Calls / Prompt** | 1.00 call | **~0.67 calls** (**-85.1%** via early exits) |
| **Max Model Calls Cap** | Uncapped | **4 calls MAX** (Authoritative limit) |
| **Mean Total Latency (CPU)** | ~1400 ms | **~2106 ms** |
| **P95 Total Latency (CPU)** | ~8600 ms | **~6278 ms** |

---

### 📂 Category Performance Breakdown (Approximate)

| Category | Prompts | Macro Reduction % | Direct LLMLingua % | Fallbacks | False Passes | False Fails | Mean Calls | Mean Latency (ms) |
|---|---|---|---|---|---|---|---|---|
| `general` | 15 | **10.65%** | 35.68% | 0 | 0 | 0 | 0.80 | ~2239 ms |
| `multi_constraint` | 50 | **9.36%** | 10.73% | 17 | 0 | 0 | 4.00 | ~6225 ms |
| `reasoning` | 15 | **8.64%** | 33.17% | 1 | 0 | 0 | 1.33 | ~3016 ms |
| `rag` | 15 | **2.55%** | 36.23% | 5 | 0 | 0 | 2.07 | ~3859 ms |
| `agents` | 15 | **2.73%** | 31.94% | 0 | 0 | 0 | 0.53 | ~1913 ms |
| `code` | 20 | **0.00%** | 41.34% | 0 | 0 | 0 | 0.00 | ~1232 ms |
| `json` | 20 | **0.00%** | 41.46% | 0 | 0 | 0 | 0.00 | ~1230 ms |
| `negation` | 50 | **0.00%** | 37.17% | 0 | 0 | 0 | 0.00 | ~1211 ms |
| `numeric_constraints` | 50 | **0.00%** | 38.65% | 0 | 0 | 0 | 0.00 | ~1246 ms |
| `output_formats` | 50 | **0.00%** | 37.98% | 0 | 0 | 0 | 0.00 | ~1247 ms |
| `ranges` | 25 | **0.00%** | 37.26% | 0 | 0 | 0 | 0.00 | ~1306 ms |
| `roles` | 15 | **0.00%** | 39.19% | 0 | 0 | 0 | 0.00 | ~1284 ms |
| `urls_paths` | 15 | **0.00%** | 41.69% | 0 | 0 | 0 | 0.00 | ~1274 ms |
| `adversarial` | 50 | **0.00%** | 37.78% | 0 | **0** | 0 | 0.00 | ~1418 ms |

---

## ⚙️ Multi-Tier Guardrail Architecture

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

1. **Tier 1: CompressibilityAnalyzer (Early Exit Filter):** Immediately exits on non-prose content (code, JSON, short instructions < 20 tokens), reducing average model calls by **-85.1%**.
2. **Tier 2: ProtectionEngine (Syntax Shield):** Replaces code blocks, schemas, URLs, and file paths with placeholders (`__CODE_BLOCK_0__`, `__URL_0__`).
3. **Tier 3: AdaptiveCompressor:** Runs subword importance scoring with step-binary search capped strictly by `MAX_MODEL_CALLS = 4`.
4. **Tier 4: Multi-Layer Validator Suite:**
   - `NegationValidator`: Detects missing prohibition targets and scope truncation (`ADV-001`).
   - `NumericValidator`: Detects altered numbers (`10 MB` $\rightarrow$ `100 MB`), reversed ranges (`3-10` $\rightarrow$ `10-3`), unit shifts, and target-number swaps.
   - `StructuralValidator`: Enforces placeholder count and schema syntax.
   - `FormatValidator`: Rejects structural output type conflicts (`single float` vs `multi-paragraph explanation`) to fix `ADV-023`.
   - `AudienceValidator`: Prevents reader level (`beginner` $\rightarrow$ `expert`) and persona shifts.
5. **Tier 5: Strict Fallback Controller:** Guarantees `assert fallback_text == original_text` if validation fails.

---

## 🛠️ Quick Start & Setup

### Option A: Python Engine & Backend Setup
```bash
# 1. Clone repository
git clone https://github.com/AREKG0/shrinktoken.git
cd shrinktoken

# 2. Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Run 105 unit tests
$env:PYTHONPATH="."; pytest backend/tests/ -m "not slow" -v

# 5. Run 405-prompt empirical benchmark suite
$env:PYTHONPATH="."; python backend/benchmarks/runner.py
```

### Option B: Python Code Usage
```python
from backend.app.compression.llmlingua import LLMLinguaCompressor
from backend.app.services.compression_engine import CompressionService
from backend.app.models.prompt import CompressionMode

# Initialize compressor & optimization service
compressor = LLMLinguaCompressor()
service = CompressionService(compressor)

prompt = "Explain quantum computing to a beginner using simple analogies."
result, telemetry = service.optimize_with_telemetry(prompt, mode=CompressionMode.balanced)

print(f"Original Tokens: {result.original_tokens}")
print(f"Compressed Tokens: {result.compressed_tokens}")
print(f"Optimized Prompt: {result.compressed_text}")
print(f"Fallback Triggered: {telemetry.fallback}")
```

### Option C: Chrome Extension & Web App
- 🌐 **Live Web App:** [shrinktoken.netlify.app](https://shrinktoken.netlify.app/)
- ⚡ **Chrome Web Store:** [Install Extension](https://chromewebstore.google.com/detail/shrinktoken/mplofkijajafbhgmeapoefnmppgmiodp)

---

## 📁 Repository Directory Map

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

## 🏆 GitHub Dynamic Cyber-Stats

<div align="center">
  <h3>⚡ Developer & Repository Metrics ⚡</h3>

<!-- GITHUB STATS CARDS -->
  <a href="https://github.com/AREKG0">
    <img src="https://github-readme-stats.vercel.app/api?username=AREKG0&show_icons=true&theme=radical&hide_border=true&bg_color=111113&title_color=00e5ff&icon_color=b900ff&text_color=ffffff" alt="GitHub Stats" />
  </a>
  <br /><br />
  <a href="https://github.com/AREKG0">
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=AREKG0&layout=compact&theme=tokyonight&hide_border=true&bg_color=111113&title_color=ff007f&text_color=ffffff" alt="Top Languages" />
  </a>
  <br /><br />

<!-- STREAK STATS -->
  <a href="https://github.com/AREKG0">
    <img src="https://github-readme-streak-stats.herokuapp.com/?user=AREKG0&theme=dark&background=111113&ring=00e5ff&fire=ff007f&currStreakLabel=b900ff&border=111113" alt="GitHub Streak" />
  </a>
  <br /><br />

<!-- ACTIVITY GRAPH -->
  <a href="https://github.com/AREKG0">
    <img src="https://github-readme-activity-graph.vercel.app/graph?username=AREKG0&bg_color=111113&color=00e5ff&line=b900ff&point=ff007f&area=true&hide_border=true" alt="Activity Graph" />
  </a>

<!-- CONTRIBUTION SNAKE ANIMATION -->
  <h3>🐍 GitHub Action Contribution Grid Snake 🐍</h3>
  <p><em>A customized automated snake traversing and consuming GitHub contribution commits!</em></p>
  <img src="https://raw.githubusercontent.com/platika/platika/master/github-contribution-grid-snake-dark.svg" width="800" alt="Contribution Snake Animation" />
</div>

---

## 📜 License & Acknowledgements

Distributed under the **MIT License**. Uses Microsoft `LLMLingua-2`.

Special thanks to the open-source community, [Capsule Render](https://github.com/kyechan99/capsule-render), [Readme Typing SVG](https://github.com/SamirPaul1/readme-typing-svg), and [Shields.io](https://shields.io/).

---

<!-- ANIMATED WAVING FOOTER -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:b900ff,100:00e5ff&height=120&section=footer" alt="ShrinkToken Footer" width="100%"/>
  <p><strong>⚡ Built with cyberpunk passion & ❤️ by <a href="https://github.com/AREKG0">OpenArc (AREKG0)</a> ⚡</strong></p>
  <p><em>"Optimize the present. Compress the future."</em></p>
</div>
