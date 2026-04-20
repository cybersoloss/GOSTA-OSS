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
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI) — or Claude Desktop with Cowork mode. Claude Code is recommended for deliberation sessions because it runs agents as parallel subprocesses with full isolation.
- Python 3.9+ (only if you want to use the reference pool semantic search tool)

### Step 1: Clone the repo

```bash
git clone <this-repo-url>
cd <repo-directory>
```

Use the clone URL from the green "Code" button at the top of this repository.

### Step 2: Start a GOSTA session

In Claude Code, from the repo root:

```
Read cowork/startup.md and start a new session.
```

This launches the interactive bootstrapper. It asks questions in groups. Below is how to answer each group for a vendor-product continuity assessment. The bootstrapper may ask additional sub-questions within each group — the guidance below covers the key decisions.

**Group 1 — Identity:**
- Session name: `vendor-assessment` (or name it after your target, e.g., `acme-product-tprm`)
- Scope: `finite`
- Complexity: `complex` (8 domain models, multi-agent deliberation)
- Mode: `code`
- Independence level: `2` (agents see each other's output but maintain independent positions)
- Deliberation: `yes`
- Shortfall logging: `yes` (recommended — captures domain model gaps during execution)
- Assessment target: your vendor and product name (e.g., "Acme Corp / Acme Platform")
- Debug logging: `no` (unless you want full agent execution traces for debugging)
- Evidence collection: `yes` (required — the session collects open-source intelligence about your target)

**Group 2 — Goal and Why:**
- Goal: "Assess whether continued dependency on [Target Vendor]'s [Target Product] represents material third-party risk. Produce a six-signal viability assessment covering business model exposure, contractual position, and dependency exposure — with dual-level scoring across 8 domains, a risk determination with timeline, and mitigation recommendations grounded in cross-domain findings."
- Why GOSTA: "Single-perspective analysis resolves cross-domain tensions silently. A vendor can score well on adaptation while its financial trajectory undermines that adaptation. Governance forces each domain to surface tensions before convergence."

**Group 2A — Analytical Frame Contract:**
The bootstrapper derives an AFC from your goal text and asks you to confirm. The correct AFC for this session:

| Field | Value |
|---|---|
| Stance | Dependent organization (existing customer) |
| Output Verb | Assess |
| Failure Mode | Unmanaged dependency |
| Prohibited Frame | Procurement advisory, competitive comparison, migration planning |

Confirm these when presented, or adjust if your situation differs.

**Group 2B — Target Reconnaissance:**
Because you named an assessment target in Group 1, the bootstrapper dispatches a reconnaissance agent to build a profile of your target vendor. It will present the profile for your review. Confirm accuracy or correct errors — the profile informs domain model suggestions and evidence collection.

**Group 3 — Domain Models:**
The bootstrapper scans the repo for available domain models and lists them. Select the eight files from this example:

```
docs/examples/vendor-product-continuity-assessment/domain-models/financial-business-health.md
docs/examples/vendor-product-continuity-assessment/domain-models/competitive-displacement.md
docs/examples/vendor-product-continuity-assessment/domain-models/adaptation-capacity.md
docs/examples/vendor-product-continuity-assessment/domain-models/saas-structural-viability.md
docs/examples/vendor-product-continuity-assessment/domain-models/structural-stickiness.md
docs/examples/vendor-product-continuity-assessment/domain-models/regulatory-entrenchment.md
docs/examples/vendor-product-continuity-assessment/domain-models/governance-strategic-coherence.md
docs/examples/vendor-product-continuity-assessment/domain-models/talent-workforce.md
```

The bootstrapper will copy them into your session directory and run a quality gate on each one. The gate may warn that some models have fewer than 6 core concepts — this is expected for models written for a specific analytical scope. Choose "proceed with warning" when prompted.

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

**Group 6 — Hypotheses:** Provide the eight hypotheses from `session-config/hypotheses.md`, or write your own based on what you already know about the target vendor.

### Step 3: Confirm and scaffold

The bootstrapper presents a summary table of all inputs. Confirm it. It then:
1. Runs a Fresh Framework Read (reads the GOSTA spec)
2. Creates the session directory under `sessions/[your-session-name]/`
3. Copies protocol files, templates, and your domain models
4. Runs the quality gate on each domain model
5. Drafts the Operating Document for your approval

The bootstrapper drafts the OD from your inputs. The pre-written OD in `session-config/operating-document.md` serves as the reference — the bootstrapper's draft should match its structure (six-signal framework, four objectives, nine guardrails). If the draft diverges from the reference, request changes to align it. The reference OD defines the Talk-2-aligned analytical structure; the bootstrapper's draft instantiates it for your specific target.

Review the OD carefully — it defines the Analytical Frame Contract (you are assessing dependency risk, not making a procurement decision), the six-signal framework, guardrails, strategy, tactics, and phase gates. Approve or request changes.

### Step 4: Collect evidence

Once the OD is approved, request evidence collection:

```
Run evidence collection for TAC-1.
```

The system dispatches collection agents to gather open-source intelligence about your target vendor and product. Each agent searches for evidence relevant to its assigned domains and tags evidence items with both domain relevance and signal relevance (which of the six signals each item informs). Evidence items are tier-classified (Tier 1: primary sources, Tier 2: authoritative analysis, Tier 3: secondary sources).

After collection completes, the system runs a directional balance check (G-6) — if more than 70% of evidence points in one direction (all "risk" or all "stable"), you review the evidence distribution before proceeding. You also review the evidence manifest to confirm adequate coverage across all six signals.

### Step 5: Run the deliberation

Once evidence is collected and reviewed, request the deliberation:

```
Run the deliberation for TAC-2.
```

In Code mode, the system creates parallel subagent processes — one per domain agent plus a coordinator. Each agent:
1. Reads its assigned domain models and evidence items
2. Produces an independent position paper with signal assessments and vendor/product scores (Round 1)
3. Reads other agents' positions and challenges their signal assessments (Round 2)
4. Converges where evidence supports it, preserves disagreements where it does not (Round 3)

The coordinator synthesizes and produces a report structured per the six-signal framework: business model signals, contractual position, dependency exposure, leading indicators, cross-domain tensions, and risk determination. You review it, approve or request changes, and the session produces the final assessment deliverable.

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
