# Is GOSTA Right for This?

A self-assessment to decide whether GOSTA fits your problem before investing time. GOSTA is not the right answer for every AI-assisted task. This page lists the signals that suggest fit, the signals that suggest poor fit, and a decision tree pointing to a starting example.

Skim the **Yes-fit** and **No-fit** signals first. If you see your problem in either column, you have your answer. If it's borderline, run the decision tree.

---

## Yes-fit signals

GOSTA is likely a good fit if **two or more** of these describe your problem:

- The decision spans **multiple domains** with potential tensions (e.g., user-value vs engineering-cost, regulatory-fit vs market-fit, candidate-skill vs culture-fit).
- The output needs to be **auditable, traceable, or reproducible** — you'll need to defend the decision later, or another reviewer will need to verify the reasoning.
- The stakes warrant **explicit hypothesis testing** — you have specific assumptions you want to test against evidence rather than confirm by default.
- You're operating in a **regulated industry, public sector, or high-accountability context** (EU AI Act, NIS2, sector-specific compliance, public funds, mission-critical decisions).
- The decision will be made under **multi-stakeholder review** — others need to see why you decided what you decided.
- AI is **making or recommending decisions** that affect real users, customers, employees, or operations — not just generating ideas.
- You want **kill conditions** before tactics start, not after they've consumed budget — pre-committed exit criteria rather than retrospective justification.
- You need the AI's **reasoning checked, not just the output** — depth, coverage, chain integrity, sycophancy detection.

## No-fit signals

GOSTA is probably **not** the right tool if any of these describe your problem:

- The task is a **single-prompt request with a stable answer** (e.g., "translate this paragraph", "explain this concept", "summarize this document"). GOSTA's overhead doesn't pay off for one-shot tasks.
- It's a **pure code-generation task** (e.g., "write a React component", "implement this algorithm"). Orchestration frameworks (LangChain, AutoGen) fit better.
- The output is **creative writing or content generation** without governance need (e.g., a blog post, an email draft, a poem). Structure adds friction without payoff.
- It's a **throwaway, one-off, low-stakes** task you'd accept any reasonable answer for. The structure costs more than the result is worth.
- You need **real-time response** — GOSTA sessions take 30 minutes minimum (simple) to multiple hours (complex deliberation). Not for chat-speed tasks.
- The problem is **single-domain with no tension** — there's only one lens to evaluate against, and the answer is mechanical (e.g., "calculate this number"). Single-prompt suffices.
- You **don't have or can't author domain models** — GOSTA's grounding mechanism requires structured domain knowledge. Without it, GOSTA reduces to generic AI with extra paperwork.
- You **don't have a Governor role** — there's no human in the loop with decision authority and time to review. GOSTA's value depends on Governor engagement at phase gates.

## Decision Tree

If neither Yes-fit nor No-fit signals are decisive, walk through these questions in order:

### Q1: Is this analytical (answer a question) or operational (produce an artifact)?

- **Analytical** (assess vendor risk, map regulatory landscape, evaluate strategic fit, audit a system): GOSTA fits — the AFC mechanism is designed for analytical scopes. Continue to Q2.
- **Operational** (build a feature, write a report, generate content): GOSTA fits if the operational decision involves multi-domain trade-offs (e.g., feature prioritization across user-value/cost/compliance). Otherwise, simpler approaches suffice. Continue to Q2 if multi-domain; otherwise GOSTA is overkill.

### Q2: Single-domain or multi-domain?

- **Single-domain** (one lens, one perspective): GOSTA is overkill unless the single domain has internal tensions (e.g., "user value" includes WTP vs activation distance vs retention — multiple sub-concepts that conflict). If so, treat sub-concepts as effective sub-domains.
- **Multi-domain** (≥2 distinct lenses likely to conflict): GOSTA fits well. Continue to Q3.

### Q3: One-time analysis or recurring cycles?

- **One-time** (finite scope, defined deliverable, then done): start with `docs/examples/feature-prioritization/` (4-agent deliberation) or `docs/examples/vendor-product-continuity-assessment/` (8-agent analytical with AFC). Single-cycle scopes complete in 30-60 min (simple) to 4-8 hr (complex deliberation).
- **Recurring** (ongoing review cadence — weekly, monthly, quarterly): GOSTA supports ongoing scopes; example artifact for this pattern is on the roadmap. Tier 0 works but is more friction than coded implementations would be.

### Q4: Do you have or can you author domain models?

- **Have ready-made domain models** (e.g., from `domain-models/examples/` or a prior session): proceed directly. Recommended starting point: `docs/examples/my-first-session/` if you're new.
- **Need to author**: budget 1-2 hr per domain model for first-time authoring. See [authoring-domain-models.md](authoring-domain-models.md). Without domain models, GOSTA reduces to generic AI with extra paperwork — domain models are the load-bearing grounding mechanism.

### Q5: Stakes — would you need to defend this decision later?

- **Yes** (regulated, public, multi-stakeholder, large $): GOSTA's audit trail justifies the structure. Configure with full deliberation, U1 reviewer at closeout, evidence collection mode if external evidence applies.
- **No** (personal, low-stakes, low-accountability): GOSTA is workable but optional. Lighter approaches (basic prompting, simple checklists) may serve.

## Borderline Cases

**"I want to use AI for personal decisions."** Career moves, major purchases, project planning. GOSTA fits if the decision is complex enough to benefit from structured analysis across multiple dimensions with traceable reasoning. It does NOT fit for 5-minute decisions where structure adds bureaucracy without payoff. Try `docs/examples/my-first-session/` to see if the structure feels right for your decision style.

**"I want governance but not the full framework."** GOSTA is layered — you can use the minimum viable subset. The Tier 0 minimum is: an Operating Document (goal + guardrails) + one domain model + a deliverable. Independence Level 1 (Governor approves every step), no deliberation, no evidence collection. Walk through `docs/examples/my-first-session/` for this minimum-viable shape.

**"My team wants AI but my boss wants control."** GOSTA's Governor role is exactly this. The framework gives the controller (boss / risk officer / compliance lead) structured oversight without micromanaging every AI interaction. Phase gates surface decisions to the Governor; signals show what the AI is producing; guardrails encode the controller's constraints. The team gets AI velocity; the controller gets oversight.

**"I'm building an AI product, not making decisions."** GOSTA governs decision-making, not product-building. If your AI product makes decisions for users (recommendation engine, automated triage, scoring system), GOSTA can govern the decision logic. If your product just generates content or executes commands, orchestration frameworks fit better.

**"I'm a researcher / academic — does GOSTA work for research?"** Yes, especially for systematic literature reviews, multi-criteria evaluations, hypothesis testing across competing theories. The framework's audit trail and reproducibility align with research norms. Public sector and policy analysis examples are on the roadmap; for now, adapt `docs/examples/feature-prioritization/` to your research question.

## Recommended Starting Points by Fit Profile

| If your problem looks like... | Start with |
|---|---|
| Personal decision, multi-factor, finite | [`my-first-session`](examples/my-first-session/) — simplest example |
| Product roadmap / feature prioritization | [`feature-prioritization`](examples/feature-prioritization/) — 4-agent deliberation |
| Vendor / supplier / dependency assessment | [`vendor-product-continuity-assessment`](examples/vendor-product-continuity-assessment/) — 8-domain analytical with AFC |
| Strategic planning with comparison | [`ciso-roadmap`](examples/ciso-roadmap/) — five-architecture comparison |
| Regulatory analysis | Adapt `vendor-product-continuity-assessment` (AFC + multi-domain analytical) — example will be on roadmap |
| Hiring decisions | Adapt `feature-prioritization` (multi-domain deliberation) with hiring rubric domain models — example on roadmap |
| Public sector / policy | Adapt `ciso-roadmap` (governed deliberation) with policy domain models — example on roadmap |

## What If You're Still Unsure?

The lowest-cost test: spend 30 minutes following the [walkthrough](walkthrough.md). It runs the simplest possible session end-to-end. By the end, you'll know whether GOSTA's structure fits how you think about decisions or feels like overhead.

If after the walkthrough you can articulate a clear "this would help me with X" — GOSTA is a fit. If you find yourself saying "this is structure for structure's sake" — it's not.

## Related

- [README](../README.md) — what GOSTA is
- [Walkthrough](walkthrough.md) — run your first session in 10 minutes
- [Examples](examples/) — completed sessions across complexity levels
- [Glossary](glossary.md) — terminology lookup
- [FAQ](faq.md) — common questions
