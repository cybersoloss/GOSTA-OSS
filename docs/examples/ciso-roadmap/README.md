# CISO Roadmap — Five-Level AI Comparison

Companion artifacts for the article **"Five Ways to Collaborate on a Security Roadmap with AI. The Last One Goes Beyond Security."**

This example runs the same CISO planning question — "How should an EU-based mid-market CISO prioritize?" — through five AI architectures, from a generic prompt to a full GOSTA governed deliberation. Inputs and outputs are published here so readers can inspect the progression.

## Structure

```
outputs/
  level1-generic-prompt.md       ← Generic AI prompt, no context
  level2-extended-reasoning.md   ← Extended reasoning (thinking mode), no context
  level3-domain-knowledge.md     ← Single prompt + 6 domain knowledge files
  level4-original-evidence.md    ← Domain files + 20 pre-selected evidence items
  level4-enhanced-evidence.md    ← Domain files + evidence + guardrails + hypotheses

domain-models/                   ← 6 structured domain knowledge files
  regulatory-compliance.md       ← NIS2 articles, cross-compliance, penalty structure
  threat-landscape.md            ← ENISA 2025, DBIR 2025, ransomware entry vectors
  operational-capacity.md        ← FTE constraints, execution bandwidth, initiative limits
  business-value-continuity.md   ← Crown jewels, recovery time reality, cyber insurance
  technology-architecture.md     ← Microsoft monoculture, identity as control plane
  supply-chain-risk.md           ← Bidirectional position, vendor assessment paradox

session-config/                  ← GOSTA session configuration (L5 only)
  operating-document.md          ← Goal, guardrails, strategy, phase gates
  deliberation-config.md         ← Agent assignments, round structure, independence level
  hypotheses.md                  ← 5 testable hypotheses (shared with L4 for fairness)
  constraints.md                 ← Hard constraints G-1 through G-5
```

## What each level demonstrates

**L1 → L2:** Extended reasoning improves sequencing but not grounding. Both produce generic priorities without domain-specific constraints.

**L2 → L3:** Domain knowledge is the largest single improvement. Priorities collapse from 10 to 5, budgets become realistic, regulatory references become specific.

**L3 → L4:** Evidence adds labeled trade-offs, but they remain generic operational categories — labels any experienced CISO would recognize without AI assistance.

**L4 → L5:** Governed multi-agent deliberation produces structurally different analysis: contested conclusions, disagreement-driven evidence retrieval, counter-factual validation, and cross-domain emergent insights. The L5 output is not published here — the session configuration documents how the governed process was set up.

## Evidence note

The L5 deliberation drew from a 575-item reference pool (219 blog articles, 328 analyst reports, 28 DBIR 2025 sections). The analyst reports are internal-only and not published here.

## Related

- [GOSTA Specification](../../../GOSTA-agentic-execution-architecture.md)
- [GOSTA Cowork Protocol](../../../cowork/gosta-cowork-protocol.md)
- [Deliberation Protocol](../../../cowork/deliberation-protocol.md)
