# Outta

> **$2/month, ~750 lines, 3 LLMs — brain-inspired AI framework**

Every response passes through Temporal lobe (context analysis) → Frontal lobe (response generation) → Cerebellum (verification + amplification).

Not a prompt chain. A signal amplification architecture inspired by how brains process information.

Built by Ham Youngjae | 2025–2026

[한국어 README](README_KR.md)

---

![demo](demo.gif)

## Why Outta

| Typical AI frameworks | Outta |
|----------------------|-------|
| LLM call for classification | Enzyme router — 0 API calls, ~30ms |
| Post-hoc hallucination filtering | 3-layer defense (code → structural → LLM) |
| Single-perspective response | Context analysis → amplification → verification |
| Prompt chaining | Brain-region signal processing |

## Performance

| Metric | Value |
|--------|-------|
| Routing speed | **~30ms** (enzyme router, 0 API calls, local embeddings) |
| FAST path | **~1s** (1 LLM call) |
| BRAIN path | **~5s** (3 LLM calls) |
| Routing accuracy | **93%** (100 independent test cases, 95% CI 88–98%) |
| Monthly cost | **~$2 API cost** (Groq free tier + DeepSeek) |
| Hallucination defense | 3-layer (pattern → structural → LLM cross-check) |
| Codebase | **~750 lines** core (excluding benchmarks/examples) |

## Architecture

```
Input
 ↓
Basal Ganglia (cache hit?) ──→ instant return
 ↓ miss
Hippocampus (inject relevant memories)
 ↓
Enzyme Router (cosine similarity, ~30ms, 0 API calls)
 ↓ confidence < threshold → Brainstem LLM fallback
FACTUAL Gate ──→ proper nouns / facts → SEARCH
 ↓
ACC (route decision)
 ├── FAST → Frontal lobe only (1 LLM call) → output
 ├── SEARCH → needs-search flag → output
 └── BRAIN ↓
      Temporal lobe (context / emotion / hidden intent)
       ↓
      Frontal lobe (context-aware response generation)
       ↓
      Cerebellum (verify + amplify)
       ↓   score < 8 → revise + reinforce
       ↓   missing perspective → amplify
      Critic (pattern blocking + structural hallucination)
       ↓
      Insula (LLM cross-check, only when score < 9)
       ↓
      Urea Cycle (pre-storage toxin filter)
       ↓
Output → Hippocampus (store) → Basal Ganglia (cache)
```

## Hallucination Defense — 3 Layers

```
Response generated
 ↓
[Layer 1] Critic — code-based pattern matching
  → fake metrics, sycophancy, axis drift, synthesis conflict, fake diversity
 ↓
[Layer 2] Insula — LLM cross-check
  → catches subtle fabrications that rules miss
 ↓
[Layer 3] Urea Cycle — pre-storage filter
  → prevents contaminated data from entering memory
```

## Quick Start

```bash
git clone https://github.com/yham5016-source/outta.git
cd outta
pip install sentence-transformers  # optional — falls back to keyword matching
```

```python
from pipeline import OuttaPipeline

pipeline = OuttaPipeline(
    llm_fast=my_fast_llm,     # lightweight: brainstem fallback (Groq Llama-70B)
    llm_think=my_think_llm,   # reasoning: temporal + frontal (DeepSeek, Qwen-235B)
    llm_verify=my_verify_llm, # verification: cerebellum + insula (use a different model)
)

result = pipeline.process("Should I quit my job?")
print(result["answer"])
# route: BRAIN | score: 9
```

### LLM Interface

```python
def my_llm(messages: list[dict], max_tokens: int, temperature: float) -> str:
    """OpenAI-compatible messages → response string."""
    ...
```

All 3 models use this interface. You can use the same model for all three — different models increase cross-verification effectiveness.

### Model Guide

| Role | Characteristics | Recommended | Why |
|------|----------------|-------------|-----|
| `fast` | Fast, cheap | Groq Llama-70B | Only used when enzyme router falls back |
| `think` | Strong reasoning | DeepSeek-V3, Qwen-235B | Response quality = overall quality |
| `verify` | Objective checker | Gemini Flash, GPT-4o-mini | Different model from think → cross-check |

## Brain Regions

### Real-time Processing

| Region | Role | File |
|--------|------|------|
| **Enzyme Router** | Cosine similarity instant classification (0 API) | `enzyme.py` |
| **Brainstem** | LLM fallback when enzyme is uncertain | `brainstem.py` |
| **ACC** | Confidence-based route branching | `acc.py` |
| **Temporal Lobe** | Context / emotion / hidden intent analysis | `temporal.py` |
| **Frontal Lobe** | Context-aware response generation | `frontal.py` |
| **Cerebellum** | Verification + missing perspective amplification | `cerebellum.py` |
| **Critic** | Pattern blocking + structural hallucination detection | `critic.py` |
| **Insula** | LLM cross-check | `insula.py` |
| **Glia** | Adaptive temperature control | `glia.py` |

### Storage

| Region | Role | File |
|--------|------|------|
| **Hippocampus** | Memory store / retrieval | `hippocampus.py` |
| **Basal Ganglia** | Pattern cache | `basal_ganglia.py` |

## Design Principles

1. **Amplify > Debate** — Role-playing opposite views with the same model is theater. Verify and reinforce a single response instead.
2. **Don't use LLMs for classification** — Cosine similarity is enough. Zero API calls.
3. **Block at generation, not post-processing** — One prompt rule beats 100 lines of regex.
4. **Never store contaminated memory** — Urea cycle. Once it's in memory, it's too late.
5. **Separate generation from verification** — The one who creates and the one who checks must be different.

## Limitations

- Routing accuracy is 93% on 100 test cases — edge cases will misroute
- "Brain-inspired" is a naming metaphor, not a neuroscience implementation
- BRAIN path adds 3 sequential LLM calls (~5s latency)
- $2/month assumes Groq free tier + Oracle Free Tier — your costs may vary
- Solo developer — maintenance bandwidth is limited
- Hippocampus uses keyword matching — no semantic search without sentence-transformers

## Benchmark

```bash
python benchmark.py
```

100 independent test cases (no overlap with router anchors):

| Category | Accuracy |
|----------|----------|
| FAST | 81.8% (27/33) |
| BRAIN | 97.1% (33/34) |
| SEARCH | 100% (33/33) |
| **Total** | **93% (93/100)** |
| 95% CI | [88%, 98%] |

## Version History

```
Outta v1 — 14-region parallel + dual amygdala signals
Outta v2 — Amplification architecture + enzyme router + structural hallucination defense
```

Key changes in v2:
- Removed dual amygdala (same-model debate is theater) → cerebellum handles amplification
- Brainstem LLM classification → enzyme router (0 API, ~30ms)
- BRAIN path: 6 LLM calls → 3 (temporal → frontal → cerebellum)
- Added structural hallucination detectors + FACTUAL gate + urea cycle
- Fixed glia temperature bug + adaptive temperature per query type

## License

Apache License 2.0

## Author

Ham Youngjae
2025–2026
