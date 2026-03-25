# Contributing to GOSTA

> **Status:** Specification stable. Tier 0 validated. Tier 1 implementation next. See the [roadmap](README.md#whats-next) for current priorities.

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

**Spec improvements** — Clarifications, corrections, or extensions to the framework specification. If proposing new sections or significant changes to existing ones, open an issue first to discuss the approach.

**Protocol enhancements** — Bug fixes, clarifications, or improvements to operational protocols. Changes should maintain backward compatibility with the existing protocol versioning scheme.

**New templates** — Additional session templates that follow the established template conventions in `templates/`.

**Domain models** — Original domain models contributed to `domain-models/examples/`. Domain models must cite their primary source (see the template in `cowork/templates/domain-model.md`). Do not submit domain models that are structured extractions of copyrighted material — original analysis grounded in publicly available knowledge is expected.

**Tools** — Improvements to existing tools or new tools that support GOSTA operations.

**Examples** — Self-contained walkthrough scenarios demonstrating GOSTA in practice.

### What We Don't Accept

- Changes that introduce dependencies on specific AI providers or orchestration frameworks. GOSTA is provider-agnostic.
- Domain models that reproduce copyrighted content without permission.
- Changes that break the framework's core separation between governance (what GOSTA does) and orchestration (what execution tools do).

## GenAI Disclosure

GOSTA was developed with significant AI assistance. The specification, protocols, documentation, and tooling were authored collaboratively between human authors and AI systems (primarily Claude). We practice what the framework governs.

If your contribution involves AI-generated content, please note this in your pull request description — including which AI tool was used, what it generated, and what you edited or validated. This isn't a gate — it's transparency. AI-assisted contributions are welcome; undisclosed AI-generated contributions are not.

## Code of Conduct

Be constructive. Critique ideas, not people. This is a governance framework — precision and clarity matter more than volume.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
