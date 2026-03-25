# Run Your First GOSTA Session

> **Status:** Beta — Specification complete. Tier 0 usable. Tier 1 implementation next.

This walkthrough takes you from zero to a working GOSTA session. You'll need an AI assistant that can read files (Claude Code, Claude Cowork, or similar).

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

If you're using Cowork mode (no terminal), just point your AI at the repo folder. It will create directories as it goes.

---

## Step 2: Start the Bootstrapper

Open a conversation with your AI assistant and paste this:

```
Read cowork/startup.md and start a new session.
```

The AI reads the startup protocol and begins asking you questions in groups. Here's what to expect and what to answer for this walkthrough:

---

### Group 1 — Identity

The AI asks for session name, scope type, complexity, mode, independence level, and deliberation preference.

**Answer:**

```
Session name: my-first-session
Scope: finite
Complexity: simple
Mode: cowork
Independence: 2
Deliberation: no
```

> **Why these choices?** Finite scope means we have a clear deliverable. Simple keeps it to 1-2 domain models. Independence 2 means the AI works autonomously within bounds but surfaces decisions. No deliberation — we'll use straightforward sequential assessment for a first session.

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

## Next Steps

**Add complexity gradually:**

- **Add a third domain model** (e.g., `regulatory-compliance`) and re-run. Watch how cross-domain tensions emerge — features that look good in two domains may score poorly in a third.
- **Enable deliberation** for a future session with 3+ domains. Each domain gets its own agent, and a coordinator synthesizes across them. See [`docs/examples/feature-prioritization/`](examples/feature-prioritization/) for a complete deliberation example with 4 agents scoring 12 features across 3 domains.
- **Try an ongoing scope** — recurring review cycles with health reports that track metric changes over time.
- **Use the session-launcher template** (`cowork/session-launcher-template.md`) instead of the interactive bootstrapper for faster setup once you're comfortable.

**Read the full framework:** `GOSTA-agentic-execution-architecture.md` §0 (Start Here) explains the five-layer hierarchy, implementation tiers, and the philosophy behind structured AI governance.
