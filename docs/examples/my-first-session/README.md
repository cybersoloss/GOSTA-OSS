# My First Session — GOSTA Walkthrough Companion

**Framework state:** Refreshed 2026-05-03 against framework v6.1 / Cowork Protocol v3.34. This is the canonical current-state example. Other examples in `docs/examples/` are version-stamped against earlier framework states and remain accurate for the disciplines they demonstrated at authoring time. See [`docs/examples/README.md`](../README.md) §"Framework-Version Compatibility" for the version-stamping convention.

A completed example of the simplest possible GOSTA session: two domain models, no deliberation, one deliverable. Use this to understand how the framework's core components fit together before tackling more complex sessions.

## What This Session Does

Prioritizes five candidate features for a single developer's next quarter (12 weeks). Two domain models — user value and engineering cost — score each feature independently. The Governor reviews scores, applies guardrails (budget constraint, no API breaking changes, no parallelization), and selects three features.

## Structure

```
00-BOOTSTRAP.md              ← Session orientation — start here
operating-document.md        ← Goal, guardrails, objectives, strategies, tactics
01-scope-definition.md       ← Initial scope negotiation

domain-models/
  user-value.md              ← How features create value for users
  engineering-cost.md        ← Effort estimation and risk factors

signals/
  scoring-user-value.md      ← Per-feature user value scores with citations
  scoring-engineering-cost.md ← Per-feature cost scores with citations

health-reports/HR-001.md     ← Session health assessment
decisions/DEC-001.md         ← Governor's final decision with rationale
deliverables/feature-ranking.md ← The deliverable: ranked feature list with recommendations
```

## How to Read This Example

Start with `00-BOOTSTRAP.md` — it orients you to the session state and lists the context loading order. Then read the operating document to see how goal, guardrails, and objectives are structured. Follow the signals to see how domain models produce scored assessments, and finish with the decision and deliverable to see the output.

This example is a snapshot of a completed session, not a template to execute. To run your own simple session, follow the [walkthrough](../../walkthrough.md).

## What to Notice

- **Every score cites domain model concepts** (G-5) — no score exists without a traceable rationale.
- **Guardrails are mechanical checks**, not suggestions. The 12-week budget (G-1) is enforced, not advisory.
- **The deliverable is the output, not the conversation.** The session produces a file (`deliverables/feature-ranking.md`), not a chat summary.

## Related

- [All Examples](../) — examples index
- [GOSTA Walkthrough](../../walkthrough.md) — step-by-step guide to running your own session
- [Feature Prioritization](../feature-prioritization/) — same problem type but with 4 agents and deliberation
