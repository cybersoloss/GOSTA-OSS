# My First Session — GOSTA Walkthrough Companion

**Framework state:** Refreshed 2026-05-03 against framework v6.1 / Cowork Protocol v3.34. This is the canonical current-state example. Other examples in `docs/examples/` are version-stamped against earlier framework states and remain accurate for the disciplines they demonstrated at authoring time. See [`docs/examples/README.md`](../README.md) §"Framework-Version Compatibility" for the version-stamping convention.

## Reproducibility Notes

A user re-executing this session today against current framework state will see the same artifact shapes (OD, signals, decisions, deliverables) but with these execution-flow differences:

- **Bootstrapper Group 1** asks 10 questions (vs the 6 visible in this example's original execution log). The 4 added flags — shortfall logging, assessment target, debug logging, evidence collection mode — were not part of the bootstrapper at this session's original authoring. For this scope they all answer "no/none."
- **Pre-Flight Validation Gates V1–V9** appear in the bootstrap output. V3 and V6 PASS; V1/V2/V4/V5 are N/A; V7/V8/V9 SKIP (no inheritance, no subagent dispatch).
- **M5 hook-availability check** at bootstrap reports PASS if hooks are installed at `.claude/settings.local.json`, WARN if not. Original execution predates the M5 mechanism.
- **M3 hook** may fire WARN if a signal file exceeds its declared cap. Per-Deliverable Caps section in the OD declares fixed caps for this session.
- **M4 hook** does NOT fire (no AFC declared, so no §12.12 Frame Integrity Validation section is expected on deliverables).
- **The deliverable does NOT need** a §12.12 Frame Integrity Validation section, §12.15 Coverage Limitations Disclosure, Verdict Strength Annotation, or Evidence Channel Disclosure — all conditional on disciplines this session's scope doesn't activate (no AFC, no deliberation, no evidence collection, no Party-X claims).

The OD has been updated to current state (Per-Deliverable Caps, Validation Manifest, Hooks reference, U1 reviewer reference). The 00-BOOTSTRAP.md and 01-scope-definition.md framework markers have been refreshed. The signals, health report, decision, deliverable, and domain models are unchanged because their format is stable across the framework versions covered by this refresh.

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
