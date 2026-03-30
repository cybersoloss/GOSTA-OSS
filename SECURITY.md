# Security Policy

## Scope

GOSTA is a specification and protocol framework — not a software application. There is no deployed service, no authentication layer, and no user data processing. The only executable code is `cowork/tools/pool-agent.py`, a local-only CLI for offline semantic search.

Security concerns in this context relate to:

- **Specification flaws** that could lead to unsafe agent behavior if implemented (e.g., missing guardrails, ambiguous governance boundaries, insufficient human oversight triggers)
- **Protocol gaps** that could allow an AI agent to bypass kill discipline, skip phase gates, or operate outside its declared autonomy level
- **Tool vulnerabilities** in `pool-agent.py` (e.g., path traversal, unsafe deserialization)

## Reporting a Vulnerability

If you discover a security issue, please report it responsibly:

1. **Email:** oss@cybersol.nl
2. **Subject line:** `[SECURITY] GOSTA — brief description`
3. **Include:** Which file/section is affected, the potential impact, and a suggested fix if you have one

We will acknowledge receipt within 72 hours and provide a substantive response within 14 days.

## What to Report

- Specification language that could be interpreted to permit unsafe autonomous behavior
- Missing or ambiguous guardrails in the governance hierarchy
- Protocol mechanics that can be circumvented by a compliant-looking agent
- Vulnerabilities in `pool-agent.py` or any contributed tooling
- Pre-commit hook bypasses that could leak private content to the public repo

## What Not to Report

- Typos or formatting issues (open a regular issue instead)
- Feature requests for new governance capabilities (open a discussion or issue)

## Disclosure Policy

We follow coordinated disclosure. Please allow us time to assess and address the issue before public disclosure. We will credit reporters in the fix commit unless anonymity is requested.
