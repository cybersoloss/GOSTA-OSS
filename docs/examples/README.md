# GOSTA Examples

Complete session examples with domain models, session configuration, and output demonstrations.

| Example | Use Case | Complexity | Domains | Deliberation |
|---|---|---|---|---|
| [my-first-session](my-first-session/) | First time with GOSTA — walkthrough companion | Simple | 2 | No |
| [feature-prioritization](feature-prioritization/) | Multi-factor product decisions with competing domain perspectives | Moderate | 3 + 1 scoped specialist | Yes (4 agents) |
| [vendor-product-continuity-assessment](vendor-product-continuity-assessment/) | Third-party vendor viability risk assessment (six-signal framework) | Complex | 8 | Yes (8 agents) |
| [ciso-roadmap](ciso-roadmap/) | CISO strategic planning — five-level AI architecture comparison | Moderate | 6 | Yes (3 agents — paired-domain configuration) |

## Applicability Map

| If you want to learn... | Start with |
|---|---|
| Tier 0 basics, OD structure, signal-to-decision flow | `my-first-session` |
| Multi-agent deliberation mechanics + cross-domain tensions + scoped specialist | `feature-prioritization` |
| Analytical Frame Contract (AFC), six-signal frameworks, evidence collection, large-scale deliberation | `vendor-product-continuity-assessment` |
| What each governance layer adds (L1 generic prompt → L5 governed deliberation), comparing architectures | `ciso-roadmap` |
| Domain model authoring (6-component structure: Core Concepts, Concept Relationships, Quality Principles, Anti-Patterns, Hypothesis Library, Guardrail Vocabulary) | Any example — all use ROBUST-tier domain models |

## Framework-Version Compatibility

Examples are dated working artifacts — each was authored against a specific framework state and remains accurate for the conceptual structure it demonstrates. The framework's deliberable-time disciplines have evolved (Verdict Strength Annotation, §12.12 Frame Integrity Validation, §12.15 Coverage Limitations Disclosure, Evidence Channel Disclosure, `[VERDICT-SPLIT-CARRIED]` annotation, formula-based per-deliverable caps); examples authored before these features may not demonstrate them. The example's `**Created:**` header indicates its authoring date. For sessions running today, expect Claude Code hooks (M1/M3/M4) to fire warnings on artifacts that miss current discipline sections — those warnings are the framework's way of guiding output toward the current standard, not a sign the example is wrong.

For a fully current example demonstrating all current disciplines, see [`my-first-session`](my-first-session/) (refreshed for the simple-session case). The other three examples are version-stamped and remain canonical for their authoring date.

## Quick-pick Guidance

**New to GOSTA?** Start with [my-first-session](my-first-session/) or the [walkthrough](../walkthrough.md).

**Want to assess a vendor?** The [vendor-product continuity assessment](vendor-product-continuity-assessment/) is a ready-to-run session template with 8 domain models, 8-agent deliberation, and a six-signal viability framework. It includes a step-by-step guide for running your own assessment. Familiarity with GOSTA basics (from the walkthrough or my-first-session) is recommended first.

**Want to see what each AI layer adds?** The [CISO roadmap](ciso-roadmap/) runs the same question through five architectures, from generic prompt to governed deliberation.

**Want to see deliberation mechanics in action?** The [feature-prioritization example](feature-prioritization/) shows 4 agents (3 domain + 1 scoped specialist) producing position papers, an interim assessment surfacing cross-domain tensions, and a synthesis report.
