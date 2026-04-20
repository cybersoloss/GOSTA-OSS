# GOSTA Architecture Guide

> **Status:** Beta — Specification complete. Tier 0 usable. Tier 1 implementation next.

This guide explains how GOSTA works — the five-layer hierarchy, implementation tiers, session lifecycle, and decision mechanics. Read it before or after the [hands-on walkthrough](walkthrough.md).

---

## The Five Layers

GOSTA organizes autonomous AI work into five layers:

![Five Layer Hierarchy](images/gosta-five-layers.gif)

**Commands flow down:** Your goal constrains what objectives are valid. Objectives constrain which strategies make sense. Strategies constrain which tactics to test. Tactics generate concrete actions.

**Feedback flows up:** Actions emit signals (data points). Tactics aggregate signals into health. Strategies validate approach logic against health data. The system surfaces structured recommendations to you.

**You are the Governor.** The AI drafts plans, executes within approved bounds, measures results, and recommends decisions. You approve, reject, or redirect. You never rubber-stamp — every decision point is structured with evidence, alternatives, and tensions.

---

## Implementation Tiers

![Implementation Tiers](images/gosta-tiers.gif)

Start with Tier 0. It requires nothing but files and a conversation. When you've validated the framework for your use case, you can invest in coded implementations (Tier 1+) that add automation, databases, and structured APIs — but the governance model stays the same.

---

## Core Documents

Before starting, skim these files (you don't need to memorize them — the AI reads them too):

| Document | What it contains | Time |
|----------|-----------------|------|
| `GOSTA-agentic-execution-architecture.md` §0 | Framework overview, tiers, how to read the spec | 10 min |
| `cowork/gosta-cowork-protocol.md` §1–5 | Session lifecycle, phases, gates | 15 min |
| `cowork/templates/operating-document.md` | What an Operating Document looks like | 5 min |

---

## How a Session Works

Every GOSTA session follows the same lifecycle. The [walkthrough](walkthrough.md) runs through this with a concrete scenario — below is the structure underneath.

### Starting a Session

There are three ways to start:

**Interactive bootstrap (recommended)** — Open a conversation with your AI assistant and say: *"Read cowork/startup.md and start a new session."* The AI asks you questions — session name, goal, scope type, complexity — and scaffolds everything.

**Template launch** — Open `cowork/session-launcher-template.md`, fill in the `{{PLACEHOLDER}}` values, paste it into a fresh AI conversation. The AI scaffolds the directory and begins Phase 0.

**Manual setup** — Create the session directory, copy templates and protocol files, then tell the AI to bootstrap:

```bash
mkdir -p sessions/my-project/{domain-models,signals,health-reports,decisions,deliverables,session-logs}
cp cowork/templates/* sessions/my-project/
cp cowork/gosta-cowork-protocol.md cowork/CLAUDE.md sessions/my-project/
```

### The Bootstrap Phase (Phase 0)

The AI:

1. **Reads the framework and protocol** — building its understanding of GOSTA
2. **Asks you clarifying questions** — scope type, complexity, what you're trying to achieve
3. **Derives an Analytical Frame Contract** (for analytical scopes) — four fields that lock the session's analytical posture and prevent the deliverable from answering the wrong question
4. **Creates or loads domain models** — pluggable knowledge files that ground the AI's reasoning in your specific domain
5. **Drafts an Operating Document (OD)** — the single document that contains your goal, guardrails, analytical frame (when applicable), objectives, strategies, tactics, and actions
6. **Presents the OD for your approval** — you review, request changes, and approve

The OD is the most important artifact. Everything downstream inherits its structure. Take the time to get it right.

Before execution begins, the AI presents a structured **Phase Gate Request**: Are all guardrails feasible? Are kill conditions discriminating? Is the domain model loaded and quality-gated? You approve, and execution begins.

### Execution Cycles (Phase 1+)

Each cycle follows the same pattern:

1. **Execute actions** — the AI performs the work defined in the OD
2. **Emit signals** — data points are logged (metrics, qualitative assessments, environmental changes)
3. **Compute health** — signals aggregate into a structured health report
4. **Present recommendations** — the AI recommends kill, pivot, or persevere for each tactic and strategy
5. **Governor decides** — you make the call at each phase gate

### Health Reports

Health reports use a traffic-light system:

| Status | Meaning |
|--------|---------|
| **GREEN** | On track. No action needed. |
| **AMBER** | Below projection but not critical. Monitor closely. |
| **RED** | Approaching or at kill threshold. Decision required. |

Every health report includes a signal-recommendation alignment check (are the recommendations consistent with the data?), risk factors (non-empty, substantive — not generic dismissals), and a sycophancy self-check (is the AI being over-optimistic?).

### Making Decisions

At each phase gate, you have three options for each tactic or strategy:

**Persevere** — continue as planned. **Pivot** — change approach while keeping the same hypothesis. **Kill** — stop this line of work entirely.

The AI presents each decision with evidence, alternatives, and tensions. Your job is to decide — not to accept the AI's recommendation uncritically.

Kill conditions exist to make kills mechanical — with bootstrap periods (don't evaluate too early), lag allowances (delayed metric impact), prerequisite checks (was the tactic actually executed?), and early triggers (kill before threshold if trajectory is unambiguous). This prevents both the sunk-cost fallacy and false kills from noisy or premature data.

### Session Closeout

When the scope is complete (finite scopes) or a major cycle ends (ongoing scopes):

1. **Final deliverables** are produced and accepted
2. **Retrospective** — what worked, what didn't, what surprised us
3. **Learnings extracted** — codified into `learnings.md` for future sessions
4. **Framework feedback** — any gaps or improvements logged for the framework itself

---

## Independence Levels and Graduation

GOSTA defines two axes of control: independence level (set at session start) and graduation stage (earned during execution).

### Independence Levels

Independence level determines how much the AI does autonomously vs. how much it checks with you:

**Level 1 — Governor-heavy.** The AI proposes every action and waits for approval before executing. Use when you're learning the framework, when stakes are high, or when you want maximum visibility. Every tactic, every score, every deliverable draft comes to you before it's final.

**Level 2 — Autonomous within bounds.** The AI executes within the approved Operating Document without asking permission for each step. It surfaces decisions only at phase gates and when guardrails are threatened. This is the default for most sessions — it balances efficiency with control.

**Level 3 — Multi-agent deliberation.** Each domain model gets its own agent, plus a coordinator who synthesizes across them. Domain agents reason independently from their domain perspective; the coordinator maps tensions, identifies disagreements, and produces a synthesis for your decision. Use for complex scopes with 3+ domains where cross-domain tensions are the primary challenge. See the [feature-prioritization example](examples/feature-prioritization/).

### Graduation Stages

Within a session, the AI starts at Stage 1 and can earn more autonomy over time:

**Stage 1** — Default. The AI drafts, you approve all strategy and tactic changes. The AI cannot create new tactics without your sign-off.

**Stage 2** — The AI can propose and execute minor tactic adjustments (timeline shifts, action resequencing) without explicit approval, but strategy changes still require Governor sign-off.

**Stage 3** — The AI can autonomously create new tactics within approved strategies. It can reallocate resources between tactics. Strategy-level changes still require Governor approval.

**Stage 4** — Full autonomous operation within the OD's guardrails. The AI creates, kills, and pivots tactics independently. The Governor reviews at phase gates and when guardrails are triggered. Reserved for proven sessions with strong track records.

Graduation is earned by demonstrating consistent quality — signals align with recommendations, guardrails are respected, and deliverables are accepted without excessive revision cycles. It's not automatic. The Governor controls whether and when to advance.

---

## Domain Model Structure

Domain models are the grounding mechanism that prevents the AI from reasoning with generic training data. Each domain model has 6 components:

**Core Concepts** — The domain's key ideas, each with a definition, boundaries (what it doesn't cover), and misapplication notes (common ways people get it wrong). Example: "Activation Distance — the number of steps between first contact and first value. Boundary: does not include ongoing engagement. Misapplication: equating fewer steps with better experience when steps provide necessary context."

**Concept Relationships** — How concepts connect: prerequisites (X must hold before Y matters), tensions (X and Y pull in opposite directions), and amplifiers (X strengthens Y). These relationships drive the cross-domain tensions that deliberation surfaces.

**Quality Principles** — Testable standards for what "good" looks like in this domain. Each principle references specific concepts and provides an observable criterion. Example: "QP-3: Effort estimates for features touching high-debt components carry a ≥1.5x multiplier."

**Anti-Patterns** — What "bad" looks like, expressed as named failure modes the AI should detect and flag. Example: "AP-1: Adoption-Retention Conflation — treating feature requests from free-tier users as evidence of willingness to pay."

**Hypothesis Library** — Testable starting points, including Governor-submitted hypotheses. Each hypothesis has a structured result format (confirmed / not confirmed / insufficient data). Governor hypotheses ensure the AI tests what the Governor cares about, not just what the data makes easy.

**Guardrail Vocabulary** — Reusable constraints that can be applied across multiple tactics. These feed into the OD's guardrail definitions.

During bootstrap, the AI quality-gates each domain model: are all 6 components present? Do concepts have boundaries? Are quality principles testable? Are anti-patterns actionable? Semantic coherence checks verify that concepts reference each other consistently and quality principles target actual concepts in the model.

---

## Deliberation

When a session uses Independence Level 3, domain assessment happens through structured multi-agent deliberation rather than sequential single-agent scoring.

### Three Roles

**Domain Agents** — One per domain model (or per scoped concept). Each agent reasons exclusively from its domain's perspective, producing a position paper that scores features/options using that domain's concepts. Domain agents don't see each other's positions during Round 1 — this ensures independence.

**Coordinator** — Has no domain model. Synthesizes across domain agents' positions, mapping agreements, soft disagreements (different scores but same directional recommendation), and hard disagreements (different directional recommendations). Produces interim assessments and a final synthesis report.

**Scoped Specialists** — Optional. A domain agent restricted to a single concept or subset. Example: a UX-1 agent that uses the market-fit model but only scores Activation Distance. Useful when a single concept needs deeper attention than it would get as one of six in a broader domain assessment.

### Round Structure

**Round 1 — Independent positions.** Each domain agent produces a position paper. The Coordinator checks for position independence (are agents genuinely reasoning independently?) and produces an interim assessment listing disagreements.

**Round 2 — Targeted responses.** Domain agents respond only to specific disagreements flagged in the interim assessment. They can revise scores, provide additional evidence, or explicitly defend their original position.

**Round 3+ — New Argument Gate.** Additional rounds require at least one genuinely new argument (a domain concept not previously cited, or a concept applied to a new angle). If no new arguments exist, deliberation terminates — remaining disagreements are structural and need Governor resolution, not more rounds.

**Synthesis.** The Coordinator produces a synthesis report with consensus items, Governor decisions (structured with options and trade-offs), resolved tensions, and a sycophancy self-check. The Governor resolves all structured decisions.

### Sycophancy Detection in Deliberation

Deliberation includes three checks against sycophantic convergence: recommendation alignment across agents (did everyone agree too quickly?), reasoning diversity (are agents using distinct logic or echoing each other?), and OD-anchoring (are agents reproducing the Operating Document's assumptions rather than independently assessing?). If Round 1 produces unanimous recommendations, a Convergence Probe Protocol triggers adversarial re-examination before accepting the consensus as genuine.

---

## Signals and Health Computation

Signals are the atomic data units that flow upward through the hierarchy.

### Signal Types

**Domain-grounded signals** — Scores, assessments, and observations derived from domain model concepts using cite-then-apply structure. Every domain-grounded signal references a specific concept, states its definition, and explains the application. This is the primary signal type in most sessions.

**Environmental signals** — External events, market shifts, regulatory changes, or new data that arrive mid-session. These aren't derived from domain models but may affect health assessments and tactic viability. Environmental signals carry a source attribution and a relevance assessment.

**Operational signals** — System-level observations about the session itself: action completion rates, retry counts, signal freshness, context utilization. These feed into the bootstrap file's state persistence fields.

### Health Computation

Signals aggregate into health reports at each phase gate. The computation follows a structured pattern: for each active tactic, the AI assesses signal-to-metric alignment (do signals support the success metrics?), kill condition proximity (how close are we to triggering the kill?), guardrail compliance (any violations or approaching violations?), and produces a RED/AMBER/GREEN assessment with a recommendation (persevere/pivot/kill).

Strategy health aggregates from tactic health: if any tactic is RED, the strategy is at risk. If the strategy's WMBT (What Must Be True) assumptions are invalidated by signal data, the strategy itself may need to be killed regardless of individual tactic health.

Every health report includes three integrity checks: signal-recommendation alignment (do the numbers match the recommendation?), non-empty risk factors (no "risks: none" when there are active tactics), and a sycophancy self-check.

---

## Key Concepts

**The Operating Document is the single source of truth.** Everything the AI does flows from it. If the OD is wrong, everything downstream is wrong.

**Domain models prevent hallucination.** Without them, the AI reasons from general training data. With them, it reasons from codified domain knowledge — 6 structured components with explicit quality principles and anti-patterns.

**Guardrails propagate downward.** A goal-level guardrail constrains every objective, strategy, tactic, and action beneath it. Hard guardrails cannot be violated. Soft guardrails can be violated with a declared recovery action.

**Signals flow upward.** Actions produce signals (domain-grounded, environmental, operational). Tactics aggregate them into health. Strategies validate logic against health data. Health reports synthesize everything into structured decisions.

**Independence and graduation control autonomy.** Independence level (1-3) sets the session's baseline control model. Graduation stages (1-4) allow earned autonomy within that model. Both are under Governor control.

**You are always in control.** The AI drafts, executes, measures, and recommends. You decide. Every decision is explicit, recorded, and reversible.

---

## Example Sessions

**[Run your first session](walkthrough.md)** — 10-minute hands-on walkthrough. Score 5 features across 2 domain models, test a hypothesis, make a governed decision.

**[Feature prioritization with deliberation](examples/feature-prioritization/)** — A multi-domain scope for an EU developer tools SaaS showing 3 domain models (market-fit, technical-feasibility, regulatory-compliance) with 16 core concepts, a 5-agent deliberation round (4 domain agents + 1 coordinator) with position papers, position independence verification, a synthesis report with 5 hard disagreements and sycophancy self-check, and Governor decisions resolving market-vs-regulatory tensions.

---

## Next Steps

- **Try it:** [Run your first session](walkthrough.md)
- **Read the spec:** `GOSTA-agentic-execution-architecture.md` — start with §0
- **Create a domain model:** Use `cowork/templates/domain-model.md` as the template
- **Explore examples:** `domain-models/examples/` has two complete domain models
