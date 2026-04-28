# Scope Definition: [Session Name]

**Created:** [date] | **Governor:** [name]
**Scope Type:** [finite | ongoing]
**Complexity:** [simple | moderate | complex]
**GOSTA Version:** v6.1
**Cowork Protocol:** v3.15
**Deliberation Protocol:** v0.9.3
**Mode:** [cowork | code | both]
**Deliberation Mode:** [enabled | disabled]

## What This Session Is

[1-2 paragraphs describing the purpose, domain, and expected outcome]

## Why GOSTA

[Why this project benefits from structured governance — what failure mode are we preventing?]

## Analytical Frame Contract
- **Stance:** [derived from goal during Group 2A]
- **Output Verb:** [derived from goal during Group 2A]
- **Failure Mode:** [derived from goal during Group 2A]
- **Prohibited Frame:** [the frame that would answer a different question — see Group 2A derivation; "—" if none]

## Domain Models Required

| Domain Model | Source | Purpose |
|---|---|---|
| [name] | [source text/book/research] | [what scoring/analysis criteria it provides] |

## Success Criteria

- [What does "done" look like for finite scopes?]
- [What does "sustained success" look like for ongoing scopes?]

## Constraints

- **Timeline:** [hard deadline? flexible?]
- **Budget:** [API credits, human hours, financial]
- **Dependencies:** [external systems, people, approvals needed]

## Risk Factors

[What could go wrong that the OD's guardrails should protect against? Each risk factor listed here should have a corresponding guardrail in the OD's Goal section. If a risk has no guardrail, either add one during OD drafting or note why it's accepted unmitigated.]

- [Risk description] → maps to: [G-N in OD, or "accepted — rationale"]

## Validation Manifest (from GOSTA §8.7)

Declared structures and their per-boundary mechanical tests. Authored at scope definition; consumed by phase-gate runner per spec §8.7.4.

| Declared Structure | Boundary | Mechanical Test | Failure Mode |
|---|---|---|---|
| <e.g., per-unit retrieval contract for Phase N> | phase entry | <e.g., 1 query per (unit, pool) cell against actual operational query set> | <BLOCK / WARN / LOG> |
| <e.g., named declared artifact at phase exit> | phase exit | <e.g., test -s <path>> | <BLOCK / WARN / LOG> |
| <e.g., continuous-capture mode-flag if active> | phase exit | <e.g., wc -l <log> vs friction signal count> | <WARN> |

Add one row per declared structure introduced by this scope. Speculative prerequisites (failure modes not empirically observed in prior sessions) are excluded per §8.7.4 anti-patterns.
