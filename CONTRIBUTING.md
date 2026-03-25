# Contributing to GOSTA

> **Status:** Beta — Specification complete. Tier 0 usable. Tier 1 implementation next. See the [roadmap](README.md#whats-next) for current priorities.

Thank you for your interest in contributing to the GOSTA framework.

## How to Contribute

### Reporting Issues

Open an issue on GitHub describing the problem. Include which part of the framework is affected (spec, protocols, templates, tools) and enough context to reproduce or understand the concern.

### Proposing Changes

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Submit a pull request with a clear description of what changed and why

### What We Accept

**Spec improvements** — Clarifications, corrections, or extensions to the framework specification (`GOSTA-agentic-execution-architecture.md`, 22 sections). For small fixes (typos, unclear wording, broken cross-references), submit a PR directly. For new sections or significant structural changes, open an issue first describing what you want to change and why — the spec's internal cross-references are dense, and changes to one section often affect others. The sync manifest (`cowork/sync-manifest.md`) tracks which protocol sections derive from which spec sections — consult it when your change touches a section listed there.

**Protocol enhancements** — Bug fixes, clarifications, or improvements to the operational protocols in `cowork/` (Cowork Protocol, Deliberation Protocol, OD Drafting Protocol). Each protocol carries a version number in its file header. Bug fixes and clarifications increment the patch version (e.g., 3.8 → 3.8.1). Changes that alter session behavior or add new mechanics increment the minor version (e.g., 3.8 → 3.9) and require a sync manifest update. Do not remove or rename existing protocol sections — downstream sessions may depend on them.

**New templates** — Additional session templates added to `cowork/templates/`. Study the existing 13 templates for conventions: markdown format, placeholder syntax (`[bracketed instructions]`), section numbering, and field names that match protocol references. New templates should include a header comment explaining when to use them and which protocol section they support.

**Domain models** — Original domain models contributed to `domain-models/examples/`. Use the template at `cowork/templates/domain-model.md` — it defines the required structure. Every domain model must include all 6 components: Core Concepts (3+ minimum, 6+ recommended), Concept Relationships, Quality Principles (3+), Anti-Patterns (2+), Hypothesis Library (2+), and Guardrail Vocabulary (2+). Cite your primary source in the header — original analysis grounded in publicly available knowledge is expected. Do not submit structured extractions of copyrighted material. See `domain-models/examples/` for two reference models that pass the quality gate.

To submit a domain model:
1. Fork the repo and create a branch
2. Copy `cowork/templates/domain-model.md` to `domain-models/examples/your-domain-name.md`
3. Build the model from your primary source following the authoring protocol in the template
4. Verify all 6 components are present and meet the minimum counts
5. Submit a PR — reviewers will check structural completeness, source citation, and analytical depth

**Tools** — Improvements to the existing reference pool agent (`cowork/tools/pool-agent.py`) or new tools that support GOSTA operations. The pool agent is the only executable code in the repo — it's a Python CLI for offline semantic search using a quantized ONNX model. Contributions here could include performance improvements, additional output formats, or new subcommands. New tools should follow the same principle: offline-first, no external API dependencies, provider-agnostic. Include usage examples and document dependencies in the tool's directory.

**Examples** — Complete worked examples added to `docs/examples/`. Each example should be a self-contained session directory showing GOSTA in practice: scope definition, operating document, domain models, and at least one deliverable. Study `docs/examples/feature-prioritization/` for the expected structure — it includes domain models, a deliberation round with position papers, a synthesis report, Governor decisions, and final deliverables. Partial examples (just a domain model, just an OD) belong in the domain models or templates categories above. Examples here should demonstrate the full session lifecycle or a significant phase of it.

### What We Don't Accept

- Changes that introduce dependencies on specific AI providers or orchestration frameworks. GOSTA is provider-agnostic.
- Domain models that reproduce copyrighted content without permission.
- Changes that break the framework's core separation between governance (what GOSTA does) and orchestration (what execution tools do).

## GenAI Disclosure

GOSTA was developed with significant AI assistance. The specification, protocols, documentation, and tooling were authored collaboratively between human authors and AI systems (primarily Claude). We practice what the framework governs.

If your contribution involves AI-generated content, note this in your pull request description — which AI tool you used and what you reviewed or rewrote. A single sentence is fine. AI-assisted contributions are welcome; undisclosed AI-generated contributions are not.

## Code of Conduct

Be constructive. Critique ideas, not people. This is a governance framework — precision and clarity matter more than volume.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
