# Run Your First GOSTA Session

> **Status:** Beta — Specification complete. Tier 0 usable. Tier 1 implementation next.

This walkthrough takes you from zero to a working GOSTA session in about 10 minutes. You'll need any AI assistant that can read files — Claude, ChatGPT, or similar.

---

## What You'll Build

A small but real governance session: deciding which 3 features to build next quarter for a product. By the end you'll have domain models, an Operating Document, domain-grounded scoring, a health report, and a Governor decision — all produced by the AI under your control.

---

## Step 1: Set Up Your Workspace

Clone the repo and create a session directory:

```bash
git clone https://github.com/cybersoloss/GOSTA-OSS.git
cd GOSTA-OSS
mkdir -p sessions/my-first-session
```

If your AI tool has direct file access (no terminal needed), just point it at the repo folder. It will create directories as it goes.

---

## Step 2: Start the Bootstrapper

Open a conversation with your AI assistant and paste this:

```
Read cowork/startup.md and start a new session.
```

The AI reads the startup protocol and begins asking you questions in groups. Here's what to expect and what to answer for this walkthrough:

---

### Group 1 — Identity

The AI asks for session name, scope shape, complexity, mode, independence, deliberation, plus four optional capability flags (shortfall logging, assessment target, debug logging, evidence collection mode). All default to off/none for a simple session.

**Answer:**

```
Session name: my-first-session
Scope: finite
Complexity: simple
Mode: cowork
Independence: 2
Deliberation: no
Shortfall logging: no
Assessment target: none
Debug logging: no
Evidence collection mode: no
```

> **Why these choices?** Finite scope means we have a clear deliverable. Simple keeps it to 1-2 domain models. Mode `cowork` (vs the default `code`) means the AI works through this conversation rather than direct file access — easier for a first session. Independence 2 means the AI works autonomously within bounds but surfaces decisions. The four "no/none" capability flags activate optional features only when needed: shortfall logging captures framework gaps for improvement cycles; assessment target enables target reconnaissance; debug logging traces agent dispatches; evidence collection mode activates the §14.8 Evidence Collection Protocol for sessions where the AI gathers external evidence. None apply for this simple roadmap session.

---

### Group 2 — Goal and Why

The AI asks what you're trying to achieve and why GOSTA is appropriate.

**Answer:**

```
Goal: Decide which 3 of these 5 features to build next quarter:
1. User onboarding wizard
2. API rate limiting
3. Dark mode
4. Audit logging
5. Bulk CSV import

Why GOSTA: Without governance, the AI will just rank by gut feel.
I want explicit criteria, scored against domain knowledge, with
constraints I control.
```

---

### Group 2A — Analytical Frame Contract (skipped for this walkthrough)

For analytical/assessment scopes (vendor evaluation, dependency exposure, regulatory mapping, etc.), the AI derives an Analytical Frame Contract (AFC) from your goal — four fields (Stance, Output Verb, Failure Mode, Prohibited Frame) that lock the session's analytical posture. This prevents the deliverable from answering the wrong question by surfacing — for example — a procurement recommendation when the goal asked for a regulatory analysis.

In this walkthrough, we're prioritizing features — an operational scope, not an analytical one — so Group 2A is skipped. For a worked example of a session where Group 2A fires (and how the AFC propagates to every agent dispatch and surfaces in deliverables via §12.12 Frame Integrity Validation), see [`docs/examples/vendor-product-continuity-assessment/`](examples/vendor-product-continuity-assessment/).

### Groups 2B / 3A / 3B (conditional — skipped for this walkthrough)

The bootstrapper has three additional conditional groups that activate only when the relevant Group 1 flag is set:
- **Group 2B — Target Reconnaissance:** runs when an assessment target is named. Performs a structured search to characterize the target before domain model selection.
- **Group 3A — Deliberation Configuration:** runs when deliberation is enabled. Configures topology, max rounds, convergence definition, sub-coordinator structure.
- **Group 3B — Evidence Collection Configuration:** runs when evidence collection mode is enabled. Configures coverage threshold, per-domain Tier 1/2 floor, adversarial collection, pool-agent integration, reference pools, web search.

None of these fire for this walkthrough since the corresponding Group 1 flags are all off. See [`docs/examples/vendor-product-continuity-assessment/`](examples/vendor-product-continuity-assessment/) for a session that exercises all three.

---

### Group 3 — Domain Models

The AI explains what domain models are — structured knowledge files that ground reasoning, not generic reference docs. It scans the repo for existing models, finds the examples in `domain-models/examples/`, and asks which to use.

**Answer:**

```
I don't have existing domain models. Create two new ones:
1. "user-value" — how users perceive and adopt features
2. "engineering-cost" — technical effort, risk, and maintenance burden
```

> **What's happening:** You're telling the AI what lenses to evaluate features through. Without domain models, it would score features using generic training data. With them, every score must trace back to a defined concept that you reviewed and approved.

---

### Group 4 — Constraints and Success

The AI asks for constraints and success criteria. Every constraint you provide will become a guardrail in the Operating Document — a hard or soft boundary that the AI must enforce.

**Answer:**

```
Constraints: 1 developer, 12 weeks budget. No breaking changes to public API.
Done means: a ranked list of 3 features with scores in both domains,
explicit trade-offs documented, and my sign-off on the final pick.
```

---

### Group 5-6 — Prior Learnings & Hypotheses

The AI scans for learnings from previous sessions (none will exist on a fresh clone) and asks for hypotheses to test.

**Answer:**

```
Skip prior learnings (first session).
Hypothesis: I think dark mode is a distraction — test whether it
scores well on user-value or if it's just noise.
```

The AI adds your hypothesis to the user-value domain model's Hypothesis Library as a Governor-submitted entry. This means it will be explicitly tested during scoring and reported on with a structured result (confirmed / not confirmed / insufficient data).

---

## Step 3: Review the Summary

The AI shows a summary table of everything you provided:

```
Session:          my-first-session
Governor:         [your name]
Date:             2026-03-25
Scope Type:       finite (simple)
Mode:             cowork
Independence:     2
Deliberation:     disabled
Analytical Frame: N/A (non-analytical scope)
Goal:             Decide which 3 of 5 features to build next quarter
Why GOSTA:        Want explicit criteria, not AI gut feel
Domain Models:    user-value (new), engineering-cost (new)
Reference Files:  none
Constraints:      1 developer, 12 weeks, no API breaking changes
Success Criteria: Ranked list of 3, dual-domain scores, trade-offs, sign-off
Prior Learnings:  skip
Hypotheses:       "Dark mode is noise" → added to user-value HL-4
```

**Say:** `Looks good, scaffold it.`

---

## Step 4: Watch the AI Build Your Session (Phase 0 — Bootstrap)

Once you confirm, the AI executes the startup protocol's Phase 3 steps. This is Phase 0 of your session — the bootstrap. The AI:

1. **Reads the protocols** — cowork protocol (`cowork/gosta-cowork-protocol.md`) and relevant framework sections (`GOSTA-agentic-execution-architecture.md` §0, §9, §21)

2. **Creates your directory structure:**
   ```
   sessions/my-first-session/
   ├── domain-models/
   ├── signals/
   ├── health-reports/
   ├── decisions/
   ├── deliverables/
   └── session-logs/
   ```

3. **Copies protocol infrastructure** — `gosta-cowork-protocol.md` and `CLAUDE.md` into your session directory. These tell the AI how to operate when it re-enters this session later.

4. **Drafts your domain models.** For each model, the AI produces a minimum viable draft with all 6 components:
   - Core Concepts (with boundaries and misapplication notes)
   - Concept Relationships (prerequisites, tensions, amplifiers)
   - Quality Principles (what "good" looks like)
   - Anti-Patterns (what "bad" looks like)
   - Hypothesis Library (testable starting points — including your Governor hypothesis)
   - Guardrail Vocabulary (reusable constraints)

   The AI presents each model for your review. You'll see something like:

   ```
   Drafted user-value.md — 6 concepts:
     Activation Distance, Retention Signal, Perceived Complexity,
     WTP Indicator, Segment Reach, Habit Formation Potential

   Quality Principles: 4
   Anti-Patterns: 3
   Hypotheses: 4 (including your Governor hypothesis as HL-4)
   Guardrails: 3

   Review this model? (say "looks good" or suggest changes)
   ```

   **Say:** `Looks good` for each model (or adjust any concepts that don't match your domain).

5. **Quality-gates the models** — checks that all 6 components are present, concepts have boundaries, quality principles are testable, and anti-patterns are actionable. If a model fails, the AI tells you what's missing and fixes it.

6. **Encodes your constraints as guardrails** — each constraint becomes a guardrail in the Operating Document:
   - 12 weeks budget → G-1 (hard, mechanical, threshold: 12 weeks)
   - 1 developer → G-2 (hard, interpretive, threshold: 1 developer — no parallelization in estimates)
   - No API breaking changes → G-3 (hard, mechanical, threshold: 0)
   - Governor sign-off → G-4 (hard, interpretive)
   - All scoring must cite domain model concepts → G-5 (hard, interpretive)

7. **Drafts the Operating Document** — goal, guardrails, objective (finite scope), strategy, tactic, actions — all populated from your inputs. The AI also creates `01-scope-definition.md` (the scope record) and `00-BOOTSTRAP.md` (session state tracker).

8. **Runs the Phase 0 Gate** — before proceeding to execution, the AI verifies readiness:
   - Domain models quality-gated? ✅
   - OD complete with all guardrails mapped to constraints? ✅
   - Governor approved summary? ✅

   If everything passes:

   ```
   Phase 0 (Bootstrap) complete. Session scaffolded:
     sessions/my-first-session/
     ├── 00-BOOTSTRAP.md
     ├── 01-scope-definition.md
     ├── operating-document.md
     ├── gosta-cowork-protocol.md
     ├── CLAUDE.md
     ├── domain-models/
     │   ├── user-value.md
     │   └── engineering-cost.md
     ├── signals/
     ├── health-reports/
     ├── decisions/
     ├── deliverables/
     └── session-logs/

   Phase 0 gate: PASS. Ready to begin Phase 1 (Assessment).
   Shall I start scoring features?
   ```

---

## Step 5: Run the Assessment (Phase 1)

**Say:** `Yes, begin.`

The AI scores each of your 5 features against both domain models. For each feature in each domain, it follows a cite-then-apply pattern: it names the domain concept, states its definition, then explains how it applies to this specific feature. You'll see something like:

```
--- Scoring F-01: User Onboarding Wizard ---

USER-VALUE DOMAIN:
  Activation Distance (steps to first value):
    Current baseline: ~5 steps. Wizard reduces to ~2.
    Drop-off data: 40% never complete setup. Score: 9

  Retention Signal (behaviors indicating ongoing value):
    Users who complete onboarding churn 40% less.
    Enables core product workflows. Score: 7

  WTP Indicator (evidence of willingness to pay):
    Cited in 3 churn interviews: "couldn't get started."
    Trial-to-paid conversion proxy. Score: 7

  [... remaining concepts ...]
  User-Value Total: 8/10

ENGINEERING-COST DOMAIN:
  Effort Estimate Confidence: High — well-understood pattern.
    Estimate: 3 weeks. No multiplier needed. Score: 8

  Dependency Chain Length: 1 — data model dependency only. Score: 8

  Reversibility: High — feature-flaggable. Score: 9

  [... remaining concepts ...]
  Engineering-Cost Total: 8/10 (feasibility)
  Effort: 3 weeks | Confidence: High | Risk: Low
```

After scoring all 5 features, the AI identifies cross-domain tensions and presents the summary:

```
Feature Scores (user-value / eng-cost / effort):

  Onboarding Wizard:  8 / 8 / 3 wk  — high value, low risk
  Bulk CSV Import:     7 / 6 / 5 wk  — strong activation, edge cases
  API Rate Limiting:   5 / 6 / 3.5wk — operational value, moderate risk
  Audit Logging:       6 / 3 / 9 wk  — compliance value, high cost [1.5x debt multiplier]
  Dark Mode:           3 / 9 / 1.5wk — low value, trivial build

Cross-Domain Tensions:
  1. Dark mode: highest feasibility (9) but lowest user-value (3).
     Governor hypothesis HL-4: CONFIRMED — below average on all 6
     user-value concepts. AP-1 (feature-request-driven development)
     detected: 8 requests, all free-tier (weak WTP signal per QP-4).

  2. Audit logging: strong user-value from enterprise (6) but
     engineering-cost score 3 due to 1.8x debt multiplier (QP-3)
     inflating base estimate from 6 weeks to 9 weeks effective.
     At 9 weeks, consumes 75% of G-1 budget.

  3. Onboarding vs. CSV import: both are activation features
     but serve different user journeys (new-user vs. migrating-user).
     Complementary, not competing — both fit in budget together.
```

---

## Step 6: Make Your Decision

The AI presents a health report and a draft recommendation, but **you decide**. It asks:

```
Recommendation (within G-1: 12-week constraint, G-2: 1 developer):

  1. Onboarding Wizard  8/8  ~3 wk
  2. Bulk CSV Import    7/6  ~5 wk
  3. API Rate Limiting  5/6  ~3.5 wk
  Total: ~11.5 weeks. G-1: PASS (0.5 wk margin).

Deferred:
  - Dark mode — user-value 3/10, HL-4 confirmed: noise
  - Audit logging — user-value 6 but effort 9 wk (doesn't fit budget)

Trade-off for Governor: Swap API Rate Limiting for Audit Logging?
  New total: ~17 weeks — exceeds G-1 by 5 weeks. VIOLATION.
  Or: Onboarding + Audit Logging only? 12 weeks — G-1 PASS but
  only 2 features, less total value (14 vs. 20 user-value).

What's your decision?
```

**Say:** `Hold the line. Approve the recommendation as-is. Log dark mode hypothesis as confirmed.`

The AI records your decision in `decisions/DEC-001.md`, produces the final health report, and marks the session complete.

---

## Step 7: Review Your Artifacts

Your session directory now contains:

```
sessions/my-first-session/
├── 00-BOOTSTRAP.md              ← Session state and history
├── 01-scope-definition.md       ← What this session is and why
├── operating-document.md        ← Governance: goal, guardrails, strategy, tactics
├── gosta-cowork-protocol.md     ← Protocol (for session re-entry)
├── CLAUDE.md                    ← AI directive (for session re-entry)
├── domain-models/
│   ├── user-value.md            ← 6-component model (6 concepts, 4 QPs, 3 APs)
│   └── engineering-cost.md      ← 6-component model (6 concepts, 4 QPs, 3 APs)
├── signals/
│   ├── scoring-user-value.md    ← Per-feature, per-concept scoring
│   └── scoring-engineering-cost.md
├── health-reports/
│   └── HR-001.md                ← GREEN/AMBER/RED tactic and strategy health
├── decisions/
│   └── DEC-001.md               ← Your sign-off with rationale
└── deliverables/
    └── feature-ranking.md       ← Scored matrix, tensions, recommendation
```

Every recommendation traces back to a domain model concept. Every decision is recorded with rationale. Nothing happened silently.

**Want to see the completed session?** The full output of this walkthrough is in [`docs/examples/my-first-session/`](examples/my-first-session/) — every file the AI produces, from domain models through scoring signals to the final decision record. (Protocol infrastructure files `gosta-cowork-protocol.md` and `CLAUDE.md` are omitted from the example to avoid duplication — in a real session, these are copied from `cowork/`.)

---

## What Just Happened

You ran a governed AI session where:

1. **You controlled the criteria** — domain models defined what "good" means, not the AI's training data
2. **Scores were grounded** — every number cites a specific domain concept and explains the application
3. **Constraints became guardrails** — the 12-week budget and single-developer constraint were hard boundaries, not suggestions
4. **Your hypothesis was tested** — dark mode was scored against the same criteria as everything else, with a structured result (confirmed: below average on all 6 user-value concepts)
5. **The decision was yours** — the AI recommended, you decided, the decision was logged with rationale

This is what GOSTA does: it makes the AI's reasoning transparent, structured, and under your control.

---

## What This Walkthrough Didn't Cover

This walkthrough used the simplest settings: 2 domain models, no deliberation, single session, Independence 2. The protocol has features that only activate with higher complexity. Here's what you'll encounter as you scale up.

### Sycophancy Detection

Every health report includes a sycophancy self-check — the AI asks itself whether it's being over-optimistic, avoiding uncomfortable recommendations, or rubber-stamping its own prior output. In the walkthrough, the dark mode scoring (3/10) demonstrates that the AI can go against what might seem like a popular choice when domain evidence says otherwise. In more complex sessions with deliberation, sycophancy detection goes further: Round 1 position independence verification checks whether domain agents are genuinely reasoning independently or echoing the Operating Document's assumptions. If unanimity is detected, a Convergence Probe forces adversarial re-examination.

### Environmental Signals

The walkthrough used only domain-model-grounded signals — scores derived directly from domain concepts. The protocol also supports environmental signals: external events, market shifts, regulatory changes, or new data that arrive mid-session and may affect health assessments. In an ongoing scope (recurring review cycles), you'd log environmental signals alongside domain signals, and they'd factor into health computation and tactic review.

### Tournament Execution

For tactics where the "right approach" isn't clear, the protocol supports tournament execution: the AI produces multiple competing deliverables (2-8 runs) against the same tactic, each exploring a different approach. In constrained tournament mode, you define a behavior space — dimensions of variation with distinct values — and each run is assigned to a specific cell. The Governor (or a selection rule) picks the winner. Tournament fields appear in the OD template under the `[ESSENTIAL]` marker. This walkthrough's scoring tactic was straightforward enough not to need it.

### Cost Tracking and Resource Ceilings

The current OD template includes `[ROBUST]` fields for resource ceilings (maximum Governor-hours or AI-hours per tactic per cycle) and cost guardrail tracking. In a multi-week ongoing scope, these become important — they prevent scope creep from consuming more Governor attention than declared capacity allows. The bootstrap file tracks cost guardrail status at session start.

### Semantic Coherence Validation

When the AI quality-gates domain models (Step 4, item 5 in this walkthrough), it checks structural completeness — are all 6 components present? Do concepts have boundaries? Are quality principles testable? Beyond this, the protocol supports semantic coherence validation: do the concepts relate to each other consistently? Do quality principles reference concepts that actually exist in the model? Are anti-patterns the inverse of quality principles or something orthogonal? This becomes critical with 3+ domain models where inconsistencies between models create scoring artifacts.

### Tier 0 State Persistence

When a session spans multiple conversations (the AI's context window resets between sessions), the bootstrap file (`00-BOOTSTRAP.md`) carries cross-session state that would be automatic at Tier 1+: action retry counters, kill deadline proximity, recovery oscillation tracking, deferred decisions, and signal absence tracking. This walkthrough completed in a single session, so these fields were trivial. In a multi-session ongoing scope, they're the mechanism that prevents the AI from losing track of failed actions, approaching deadlines, or unresolved issues.

### Independence Levels and Graduation

This walkthrough used Independence Level 2 (the AI works autonomously within approved bounds but surfaces decisions). Level 1 means the Governor reviews every action before execution. Level 3 enables multi-agent deliberation — each domain model gets its own agent, plus a coordinator who synthesizes across them. See the [feature-prioritization example](examples/feature-prioritization/) for a Level 3 session.

Within a session, graduation stages (1-4) control how much autonomy the AI earns over time. Stage 1 is the default — Governor approves all strategy and tactic changes. At Stage 3+, the AI can autonomously create tactics within approved strategies. Graduation is earned by demonstrating consistent quality, not assumed.

### Analytical Frame Contract (AFC) for Analytical Scopes

This walkthrough is operational (prioritizing features). Analytical scopes (vendor assessment, regulatory mapping, market analysis) trigger Group 2A, which derives a four-field AFC (Stance / Output Verb / Failure Mode / Prohibited Frame) that constrains every agent dispatch and surfaces in deliverables via a `## Frame Integrity Validation` section (§12.12). The AFC prevents drift — e.g., an assessment of a vendor surfacing as a buyer's procurement recommendation. See [`docs/examples/vendor-product-continuity-assessment/`](examples/vendor-product-continuity-assessment/).

### Evidence Collection Mode

For sessions that gather external evidence (vendor research, regulatory text, market reports), Group 1's `evidence collection mode = yes` activates the §14.8 Evidence Collection Architecture and Group 3B configuration. The AI dispatches collection agents per domain, each producing structured evidence items with tier classifications, citation discipline, and counter-framing for adversarial collection. Coverage is audited against a Governor-set threshold; sub-threshold coverage produces a `## Coverage Limitations Disclosure` section (§12.15) in deliverables.

### Independent Reviewer (U1)

Sessions with deliberation or analytical scopes can dispatch a U1 independent-reviewer subagent at phase-gate decision support and at closeout. U1 has no domain model — it audits the orchestrator's claims against actual files, looking for file-grounding violations, AFC consistency, sycophancy patterns, and binding-precondition annotations. U1 produces a PASS / FAIL / PASS-WITH-NOTES verdict that the Governor uses for disposition.

### Claude Code Hooks (Optional Mechanizable-Discipline Layer)

When running GOSTA sessions in Claude Code, optional hooks fire on Task / Write / Edit / SessionEnd events to enforce mechanizable disciplines: M1 checks signal-first execution before agent dispatch, M3 checks per-deliverable cap overage, M4 checks AFC section presence on deliverable production, plus log-dispatch and audit-closeout hooks for trace and closeout verification. Install via `cp cowork/templates/hooks-settings.json ~/.claude/settings.local.json` (or per-project in `.claude/settings.local.json`). Hooks are advisory at write-time and structural at closeout.

---

## Next Steps

**Add complexity gradually:**

- **Add a third domain model** (e.g., `regulatory-compliance`) and re-run. Watch how cross-domain tensions emerge — features that look good in two domains may score poorly in a third.
- **Enable deliberation** for a future session with 3+ domains. Each domain gets its own agent, and a coordinator synthesizes across them. See [`docs/examples/feature-prioritization/`](examples/feature-prioritization/) for a complete deliberation example with 5 agents (4 domain + 1 coordinator) scoring 12 features across 3 domains, with position independence verification and sycophancy checks.
- **Try an ongoing scope** — recurring review cycles with health reports that track metric changes over time. This is where environmental signals, cost tracking, and Tier 0 state persistence become essential.
- **Try tournament execution** — for a tactic where the approach is uncertain, add tournament fields to the OD and have the AI produce competing deliverables.
- **Use the session-launcher template** (`cowork/session-launcher-template.md`) instead of the interactive bootstrapper for faster setup once you're comfortable.

**Try a public interest scenario:** Municipal budget allocation, policy analysis, sustainability planning — domains where decisions carry public accountability and auditability requirements. Public sector and sustainability examples are on the [roadmap](../README.md#whats-next).

**Understand the architecture:** The [Architecture Guide](architecture-guide.md) explains the five-layer hierarchy, implementation tiers, independence levels, graduation stages, deliberation mechanics, and decision mechanics with diagrams.

**Read the full framework:** `GOSTA-agentic-execution-architecture.md` §0 (Start Here) for the complete specification.
