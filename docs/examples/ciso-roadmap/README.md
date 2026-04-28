# CISO Roadmap — Five-Level AI Comparison

Companion artifacts for the article **"Five Ways to Build a Security Roadmap with AI — The Last One Changes the Decision."**

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

## Replicate this

You can run your own version of this CISO roadmap session. The domain models and session configuration published here are the actual inputs — you supply the AI execution environment.

### Prerequisites

- Git
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI) — or Claude Desktop with Cowork mode. Claude Code is recommended for deliberation sessions because it runs agents as parallel subprocesses with full isolation.
- Python 3.9+ (only if you want to use the reference pool semantic search tool)

### Step 1: Clone the repo

```bash
git clone https://github.com/cybersoloss/GOSTA-OSS.git
cd GOSTA-OSS
```

### Step 2: Start a GOSTA session

In Claude Code, from the repo root:

```
Read cowork/startup.md and start a new session.
```

This launches the interactive bootstrapper. It will ask you questions in groups. Here is how to answer them to replicate this specific session:

**Group 1 — Identity:**
- Session name: `ciso-roadmap` (or any name you prefer)
- Scope: `finite`
- Complexity: `complex` (6 domain models, multi-agent)
- Mode: `code`
- Independence level: `2`
- Deliberation: `yes`
- Shortfall logging: `yes` (recommended — captures domain model gaps)

**Group 2 — Goal and Why:**
- Goal: "Produce a multi-domain CISO priority assessment for EU-based mid-market organizations (50–500 employees) that surfaces cross-domain tensions, competing priorities, and sequencing constraints."
- Why GOSTA: "Single-prompt analysis produces plausible priorities that collapse when cross-domain constraints are applied. Governance forces each domain to surface tensions before convergence."

**Group 3 — Domain Models:**
- When asked which existing models to reuse: `none`
- When asked about new domain models: point the bootstrapper to the six files in this example:

```
docs/examples/ciso-roadmap/domain-models/regulatory-compliance.md
docs/examples/ciso-roadmap/domain-models/threat-landscape.md
docs/examples/ciso-roadmap/domain-models/operational-capacity.md
docs/examples/ciso-roadmap/domain-models/business-value-continuity.md
docs/examples/ciso-roadmap/domain-models/technology-architecture.md
docs/examples/ciso-roadmap/domain-models/supply-chain-risk.md
```

The bootstrapper will copy them into your session directory and run a quality gate on each one. The gate will warn that most models have 4–5 core concepts (the minimum is 6). This is expected — these models were built for a specific analytical scope. Choose "proceed with warning" when prompted.

**Group 3A — Deliberation Configuration:**
The bootstrapper will auto-generate an agent roster from your domain models. To match this example, you want three agents with two domain models each:

- Agent A (Regulatory-Operational): regulatory-compliance + operational-capacity
- Agent B (Threat-Technology): threat-landscape + technology-architecture
- Agent C (Business-Supply Chain): business-value-continuity + supply-chain-risk
- Coordinator: COORD-1 (auto-generated, no domain model)

For cadence: trigger `on_governor_request`, max rounds `4`, new argument gate enabled, governor interaction `at_synthesis`.

**Group 4 — Constraints:**
- Use the constraints from `docs/examples/ciso-roadmap/session-config/constraints.md` — or state them directly: no vendor names, EU-specific grounding, mid-market feasibility (0.5–3 FTE, €50K–€300K budget), no implementation guides.
- Success criteria: cross-domain tensions explicitly identified, priority sequencing accounts for execution bandwidth, at least 3 non-obvious insights that single-domain analysis would miss.

**Group 5 — Prior learnings:** skip (first session)

**Group 6 — Hypotheses:** Provide the five hypotheses from `docs/examples/ciso-roadmap/session-config/hypotheses.md`, or state your own.

### Step 3: Confirm and scaffold

The bootstrapper presents a summary table. Confirm it. It then:
1. Runs a Fresh Framework Read (reads the GOSTA spec)
2. Creates the session directory under `sessions/ciso-roadmap/`
3. Copies protocol files, templates, and your domain models
4. Runs the quality gate on each domain model
5. Drafts the Operating Document for your approval

Review the OD carefully — it defines guardrails, strategy, tactics, and phase gates. Approve or request changes.

### Step 4: Run the deliberation

Once the OD is approved, request the deliberation:

```
Run the deliberation for TAC-1.
```

In Code mode, the system creates parallel subagent processes — one per domain agent plus a coordinator. Each agent:
1. Reads its assigned domain models
2. Produces an independent position paper (Round 1)
3. Reads other agents' positions and challenges them (Round 2)
4. Converges where evidence supports it (Round 3)
5. Audits dependencies and runs counter-factual reversal tests (Round 4)

The coordinator synthesizes after each round and produces a final synthesis report for you. You review it, approve or request changes, and the session produces the final deliverable.

### Step 5 (optional): Reference pool

The original session drew from a 575-item reference pool during deliberation. You can run the session without a reference pool — agents will reason from domain models alone. If you want to add your own evidence sources:

```bash
# Install runtime dependencies (required for query, build, index-doc, update)
pip3 install numpy pyyaml onnxruntime tokenizers

# Install setup-model-only dependencies (one-time, beyond runtime)
pip3 install huggingface-hub onnx

# Download and quantize the embedding model (one-time, ~22MB result)
python3 cowork/tools/pool-agent.py setup-model

# Build a vector store from your articles directory
python3 cowork/tools/pool-agent.py build \
    --pool your-pool.yaml \
    --articles ./your-sources/ \
    --store ./your-pool-store/

# Query during session
python3 cowork/tools/pool-agent.py query "vendor MFA dependency" \
    --store ./your-pool-store/ \
    --top 10
```

The pool YAML format and article structure are documented in the [GOSTA specification §18](../../../GOSTA-agentic-execution-architecture.md).

### What to expect

Your results will differ from this example. The domain models are the same, but deliberation is non-deterministic — agents may surface different tensions, retrieve different evidence, and reach different dependency conclusions. That is expected. The value is in the governed process producing contested, traceable reasoning — not in reproducing identical outputs.

The L1–L4 outputs published here (`outputs/`) can serve as a baseline to compare against your own L5 results.

## Related

- [GOSTA Specification](../../../GOSTA-agentic-execution-architecture.md)
- [GOSTA Cowork Protocol](../../../cowork/gosta-cowork-protocol.md)
- [Deliberation Protocol](../../../cowork/deliberation-protocol.md)
