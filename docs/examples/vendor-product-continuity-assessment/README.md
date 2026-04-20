# Vendor-Product Continuity Assessment — GOSTA Session Template

A ready-to-run GOSTA session template for assessing whether continued dependency on a vendor's product represents material third-party risk. Copy this directory, replace the placeholders with your target vendor and product, and execute.

This session implements the analytical framework from **"Breach Risk Is Scored. Survival Risk Is Not."** — six observable vendor viability signals, eight analytical domain models, four-agent deliberation, and a structured risk determination. The session is designed to produce exactly the analysis the framework describes: business model viability, contractual position, dependency exposure, and leading indicator assessment.

## Structure

```
00-BOOTSTRAP.md                             ← Session orientation — start here
session-config/
  operating-document.md                     ← Goal, AFC, six-signal framework, objectives, strategies, tactics
  deliberation-config.md                    ← 4 agents, signal coverage map, tension requirements
  hypotheses.md                             ← 8 testable hypotheses mapping framework claims
  constraints.md                            ← Hard/soft constraints and scope exclusions

domain-models/                              ← 8 structured domain knowledge files
  financial-business-health.md              ← ECON-1: Revenue trajectory, SaaS metrics, failure thresholds
  competitive-displacement.md               ← DISP-1: AI displacement, platform bundling, data moat
  adaptation-capacity.md                    ← ADAPT-1: R&D investment, vendor-product divergence detection
  saas-structural-viability.md              ← SAAS-1: Pricing vulnerability, platform vs. shelfware
  structural-stickiness.md                  ← STICK-1: Migration complexity, stickiness-viability matrix
  regulatory-entrenchment.md                ← REG-1: Regulatory moat, exit provisions, DORA/NIS2
  governance-strategic-coherence.md         ← GOV-1: Leadership stability, acquirer patterns
  talent-workforce.md                       ← TAL-1: Talent pipeline, retention signals, workforce capacity

outputs/                                    ← Quality progression demonstration (supplementary)
  level1-generic-prompt.md                  ← Generic AI prompt, no context
  level2-extended-reasoning.md              ← Extended reasoning (thinking mode), no context
  level3-domain-knowledge.md                ← Single prompt + 8 domain model files
  level4-deliberation-assessment.md         ← Full GOSTA multi-agent deliberation
```

## The Six Signals Framework

The session assesses vendor viability through six observable signals grouped into three categories. This framework defines what the session must produce — every signal receives an evidence-grounded assessment.

### Category 1 — Business Model Signals (Is the vendor structurally viable?)

| Signal | What It Assesses | Domain Coverage |
|---|---|---|
| **(1) Revenue model exposure** | Is the vendor pricing per-seat for capabilities that AI can now automate, or pricing on differentiated outcomes? | SAAS-1 + ECON-1 |
| **(2) Domain depth vs. feature breadth** | Does the product operate on customer-specific data (defensible moat) or publicly available knowledge (substitution risk)? | DISP-1 (Data Moat) |
| **(3) Financial sustainability / consolidation** | Is the vendor a consolidation winner or acquisition target? Is capital concentrating toward or away from their category? | ECON-1 |

### Category 2 — Contractual Position (Are you protected if they fail?)

| Signal | What It Assesses | Domain Coverage |
|---|---|---|
| **(4) Exit strategy provisions** | Does the contract include data portability, transition assistance, source code escrow? DORA Article 28 compliant? | REG-1 |
| **(5) Regulatory embedding depth** | Is the vendor embedded in compliance workflows (audit trails, evidence, notification chains) or outside the compliance-critical path? | REG-1 |

### Category 3 — Dependency Exposure (How much operational risk do you carry?)

| Signal | What It Assesses | Domain Coverage |
|---|---|---|
| **(6) Vendor stickiness vs. viability** | If the vendor ceased operations, how long are you stuck? High stickiness + low viability = maximum risk. | STICK-1 |

### Leading Indicators (predict viability deterioration before Signals 1-6 manifest)

| Domain | Role |
|---|---|
| TAL-1 (Talent & Workforce) | Talent departures precede financial deterioration by 2-4 quarters |
| GOV-1 (Governance) | Leadership instability predicts operational deterioration 12-18 months ahead |
| ADAPT-1 (Adaptation Capacity) | Assesses whether the vendor can respond to identified pressures |

## The Eight Domain Models

The domain models form four agent pairs designed to create productive friction during deliberation:

| Agent | Name | Domains | Signal Coverage |
|---|---|---|---|
| A | Business Model Analyst | ECON-1 + DISP-1 | Signals 1, 2, 3 |
| B | Structural Viability Analyst | ADAPT-1 + SAAS-1 | Signal 1 depth + adaptation |
| C | Dependency Exposure Analyst | STICK-1 + REG-1 | Signals 4, 5, 6 |
| D | Leading Indicator Analyst | GOV-1 + TAL-1 | Forward-looking early warning |

Financial pressure (ECON-1) constrains adaptation capacity (ADAPT-1). High stickiness (STICK-1) can mask declining viability (ECON-1 + DISP-1). Regulatory moats (REG-1) protect vendor demand but amplify exit costs (STICK-1). Talent signals (TAL-1) provide early warning of governance opacity (GOV-1) and product deprioritization before they manifest in financial metrics. The deliberation protocol forces these tensions to surface explicitly rather than being silently resolved by a single analyst.

## Run Your Own Assessment

### Prerequisites

- Git
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) (CLI) — install with `npm install -g @anthropic-ai/claude-code`. Or use Claude Desktop with Cowork mode. Claude Code is recommended for deliberation sessions because it runs agents as parallel subprocesses with full isolation.
- Python 3.9+ (recommended if you plan to use the reference pool for semantic search over your own evidence sources; not required for the core session)

### Step 1: Clone and prepare

```bash
git clone <this-repo-url>
cd <repo-directory>
```

Use the clone URL from the green "Code" button at the top of this repository.

Before starting the bootstrapper, copy the domain models from this example into the repo's shared domain models directory so the bootstrapper can discover them:

```bash
cp docs/examples/vendor-product-continuity-assessment/domain-models/*.md domain-models/
```

This makes the eight domain models available when the bootstrapper scans for reusable models. You can remove them from `domain-models/` after your session is scaffolded — the bootstrapper copies selected models into your session directory.

### Step 2: Start a GOSTA session

In Claude Code (the CLI), from the repo root, type this as a prompt to the AI:

```
Read cowork/startup.md and start a new session.
```

This launches the interactive bootstrapper. It asks questions in groups — one group at a time. Below is how to answer each group for a vendor-product continuity assessment. The bootstrapper may ask additional sub-questions within each group — the guidance below covers the key decisions.

If you are using Claude Desktop with Cowork mode instead of the CLI, the same prompt works — type it in the conversation. Claude Code CLI is recommended for deliberation sessions because it runs agents as parallel subprocesses with full isolation.

**Group 1 — Identity:**
- Session name: `vendor-assessment` (or name it after your target, e.g., `drata-platform-tprm`)
- Scope: `finite`
- Complexity: `complex` (8 domain models, multi-agent deliberation)
- Mode: `code`
- Independence level: `2` (agents see each other's output but maintain independent positions)
- Deliberation: `yes`
- Shortfall logging: `yes` (recommended — captures domain model gaps during execution)
- Assessment target: your vendor and product name (e.g., "Drata / Drata Platform")
- Debug logging: `no` (unless you want full agent execution traces for debugging)
- Evidence collection: `yes` (required — the session collects open-source intelligence about your target)

**Group 2 — Goal and Why:**
Replace the vendor and product names in the goal text with your actual target before pasting:
- Goal (example for Drata): "Assess whether continued dependency on Drata's Drata Platform represents material third-party risk. Produce a six-signal viability assessment covering business model exposure, contractual position, and dependency exposure — with dual-level scoring across 8 domains, a risk determination with timeline, and mitigation recommendations grounded in cross-domain findings."
- Why GOSTA: "Single-perspective analysis resolves cross-domain tensions silently. A vendor can score well on adaptation while its financial trajectory undermines that adaptation. Governance forces each domain to surface tensions before convergence."

**Group 2A — Analytical Frame Contract:**
The bootstrapper derives an AFC from your goal text and asks you to confirm. Review carefully — the AFC controls the analytical frame for the entire session. The correct AFC for a vendor continuity assessment:

| Field | Value |
|---|---|
| Stance | Dependent organization (existing customer) |
| Output Verb | Assess |
| Failure Mode | Unmanaged dependency |
| Prohibited Frame | Procurement advisory, competitive comparison, migration planning |

Confirm if the bootstrapper's derivation matches this. If it differs, correct it before proceeding — the AFC propagates to every objective, strategy, and agent dispatch.

**Group 2B — Target Reconnaissance:**
Because you named an assessment target in Group 1, the bootstrapper dispatches a reconnaissance agent to build a profile of your target vendor. This takes 1-2 minutes. The bootstrapper presents the profile for your review — confirm accuracy or correct errors. The profile informs domain model suggestions and evidence collection strategy.

**Group 3 — Domain Models:**
The bootstrapper scans the repo for available domain models and lists them numbered. Because you copied the domain models into `domain-models/` in Step 1, all eight will appear in the list. Select all eight:

- `financial-business-health.md` (ECON-1)
- `competitive-displacement.md` (DISP-1)
- `adaptation-capacity.md` (ADAPT-1)
- `saas-structural-viability.md` (SAAS-1)
- `structural-stickiness.md` (STICK-1)
- `regulatory-entrenchment.md` (REG-1)
- `governance-strategic-coherence.md` (GOV-1)
- `talent-workforce.md` (TAL-1)

When asked about adaptation intent for each model, choose `adapt` — the bootstrapper will update application context headers for your specific target. The quality gate may warn that some models have fewer than 6 core concepts — this is expected for models written for a specific analytical scope. Choose "proceed with warning" when prompted.

**Group 3A — Deliberation Configuration:**
The bootstrapper auto-generates an agent roster from your domain models. To match the recommended pairing:

- Agent A (Business Model Analyst): ECON-1 + DISP-1
- Agent B (Structural Viability Analyst): ADAPT-1 + SAAS-1
- Agent C (Dependency Exposure Analyst): STICK-1 + REG-1
- Agent D (Leading Indicator Analyst): GOV-1 + TAL-1
- Coordinator: COORD-1 (auto-generated)

Four agents with paired domains produce structured disagreement across all eight domain models and all six signals. For cadence: trigger `on_governor_request`, max rounds `3`, new argument gate enabled, governor interaction `at_synthesis`.

**Group 3B — Evidence Collection Configuration:**
Since you enabled evidence collection in Group 1, the bootstrapper asks about collection setup. Recommended answers:
- Topology: `single-target` (you are assessing one vendor)
- Agent count: accept the computed default (typically 5-6 agents: one per domain pair + discovery + adversarial)
- Adversarial collection: `counter-framing` (generates counter-hypotheses to prevent confirmation bias)
- Evidence quality audit: `directional` (checks for sycophantic over-collection of confirming evidence, threshold 70%)
- URL verification: accept defaults (100% Tier 1, 30% Tier 2)

**Group 4 — Constraints:**
- Use the constraints from `session-config/constraints.md` — or state directly: dependency risk frame only (no procurement advice), six-signal coverage required, evidence-grounded scoring, dual-level assessment (vendor + product independently), single-session scope.
- Success criteria: all 6 signals scored with evidence citations, cross-domain tensions explicitly identified, risk determination with timeline, leading indicator assessment, at least 3 mitigation recommendations grounded in multiple domains.

**Group 5 — Prior learnings:** skip (first session). If you have run prior GOSTA sessions, select relevant learnings files when the bootstrapper lists them.

**Group 6 — Hypotheses:** Provide the eight hypotheses from `session-config/hypotheses.md`, or write your own based on what you already know about the target vendor. Replace `[Target Vendor]` and `[Target Product]` with your actual target when pasting.

### Step 3: Confirm and scaffold

The bootstrapper presents a summary table of all inputs. Review it and confirm. It then:
1. Runs a Fresh Framework Read (reads the GOSTA spec)
2. Creates the session directory under `sessions/[your-session-name]/`
3. Copies protocol files, templates, and your domain models
4. Runs the quality gate on each domain model
5. Drafts the Operating Document for your approval

The bootstrapper drafts an OD from your inputs. For the Talk-2-aligned session, tell the bootstrapper to use the pre-written OD as the starting point:

> Use the OD from `docs/examples/vendor-product-continuity-assessment/session-config/operating-document.md` as the template. Replace `[Target Vendor]` with Drata and `[Target Product]` with Drata Platform throughout.

This gives the bootstrapper the six-signal framework, four objectives (OBJ-1 through OBJ-4), nine guardrails (G-1 through G-9), and the Talk-2-aligned deliverable structure — all pre-written and tested. The bootstrapper will copy it into your session directory, substitute your target, and present it for your approval. This is faster and more reliable than having the bootstrapper draft from scratch.

Review the OD carefully — it defines the Analytical Frame Contract, the six-signal framework, guardrails, strategy, tactics, and phase gates. Approve or request changes. The bootstrapper will not proceed until you approve.

### Step 4: Collect evidence

Once the OD is approved, the bootstrapper presents a Phase Gate (Phase 0 → Phase 1). Approve it to advance. The bootstrapper confirms the session is active and ready for execution. From this point, you are in the live session — continue in the same conversation.

Say to the AI:

```
Run evidence collection for TAC-1.
```

The system dispatches collection agents to gather open-source intelligence about your target vendor and product. Each agent searches for evidence relevant to its assigned domains and tags evidence items with both domain relevance and signal relevance (which of the six signals each item informs). Evidence items are tier-classified (Tier 1: primary sources, Tier 2: authoritative analysis, Tier 3: secondary sources).

After collection completes, the system runs a directional balance check (G-6) — if more than 70% of evidence points in one direction (all "risk" or all "stable"), you review the evidence distribution before proceeding. You also review the evidence manifest to confirm adequate coverage across all six signals. Approve the evidence base before moving to deliberation.

### Step 5: Run the deliberation

Once evidence is collected and reviewed, say to the AI:

```
Run the deliberation for TAC-2.
```

In Code mode, the system creates parallel subagent processes — one per domain agent plus a coordinator. Each agent:
1. Reads its assigned domain models and evidence items
2. Produces an independent position paper with signal assessments and vendor/product scores (Round 1)
3. Reads other agents' positions and challenges their signal assessments (Round 2)
4. Converges where evidence supports it, preserves disagreements where it does not (Round 3)

The coordinator synthesizes and produces a report structured per the six-signal framework: business model signals, contractual position, dependency exposure, leading indicators, cross-domain tensions, and risk determination. You review it, approve or request changes, and the session produces the final assessment deliverable.

The final report is saved to `sessions/[your-session-name]/deliverables/`. The session also retains the full deliberation transcript, evidence manifest, and per-agent position papers in the session directory for audit and traceability.

### Step 6 (optional): Reference pool

You can enhance evidence quality by building a semantic search pool from your own sources (analyst reports, vendor documentation, financial filings, regulatory guidance) before running evidence collection:

```bash
pip3 install numpy pyyaml onnxruntime

# First-time: download and quantize the embedding model
pip3 install tokenizers huggingface-hub onnx
python3 cowork/tools/pool-agent.py setup-model

# Build a vector store from your sources
python3 cowork/tools/pool-agent.py build \
    --pool your-pool.yaml \
    --articles ./your-sources/ \
    --store ./your-pool-store/

# Query during session
python3 cowork/tools/pool-agent.py query "vendor financial runway analysis" \
    --store ./your-pool-store/ \
    --top 10
```

The pool YAML format and article structure are documented in the [GOSTA specification §18](../../../GOSTA-agentic-execution-architecture.md).

## Adapting the Domain Models

The eight domain models are written for SaaS vendor-product assessments. If your target operates in a different model, you may want to adapt:

- **Non-SaaS vendors:** SAAS-1 (SaaS Structural Viability) can be replaced with a model covering the relevant business model risks (e.g., hardware supply chain, perpetual license economics, managed service dependency).
- **Non-technology vendors:** DISP-1 (Competitive Displacement) and ADAPT-1 (Adaptation Capacity) are technology-focused. Replace or modify the concepts for your vendor's industry.
- **Regulated industries:** REG-1 references DORA, NIS2, and GDPR. Substitute the regulatory frameworks relevant to your industry and jurisdiction.
- **TAL-1 is vendor-type-agnostic:** Unlike SAAS-1 or DISP-1 which are technology-focused, TAL-1 (Talent & Workforce) applies across all vendor types — technology, professional services, manufacturing, consulting. Key personnel stability, retention patterns, and workforce capacity trajectory are universal leading indicators of organizational health regardless of industry.
- **Adding domains:** The framework supports any number of domain models. Add industry-specific domains (e.g., supply chain resilience, environmental compliance, data sovereignty) as needed.

When adapting, maintain the domain model structure: core concepts with boundaries and common misapplications, concept relationships (prerequisites, tensions, amplifiers), quality principles, and anti-patterns. This structure is what enables the quality gate and deliberation protocol to function.

## Quality Progression Demonstration

The `outputs/` directory contains four output levels showing what each layer of AI architecture adds when applied to a generic vendor assessment:

**L1 → L2:** Extended reasoning adds causal chains and rudimentary cross-category connections, but both levels produce generic risk categories pulled from training data. Neither distinguishes vendor-level from product-level risk.

**L2 → L3:** Domain models are the largest single improvement. Generic categories sharpen into specific analytical constructs: SaaS failure-trajectory flags replace vague "financial health" assessments, displacement timelines replace "competitive pressure," and the stickiness-viability combination matrix produces risk determinations that flat lists cannot express.

**L3 → L4:** Governed multi-agent deliberation produces structurally different analysis: each domain agent independently scores and defends positions, cross-domain tensions surface through forced disagreement, evidence attribution chains trace every finding to sources, and the Governor's guardrails prevent analytical frame drift. Emergent findings — conclusions that no single domain agent would produce independently — appear from domain collision.

### What to expect

Your results will differ from the example outputs. Deliberation is non-deterministic — agents may surface different tensions, retrieve different evidence, and reach different conclusions. That is expected. The value is in the governed process producing contested, traceable, evidence-grounded reasoning — not in reproducing identical outputs.

## Related

- [GOSTA Specification](../../../GOSTA-agentic-execution-architecture.md)
- [GOSTA Cowork Protocol](../../../cowork/gosta-cowork-protocol.md)
- [Deliberation Protocol](../../../cowork/deliberation-protocol.md)
- [CISO Roadmap Example](../ciso-roadmap/) — different session type (strategic planning vs. vendor assessment)
