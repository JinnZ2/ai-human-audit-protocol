# Security Policy

## Scope

This repository defines symbolic protocols for ethical AI-human interaction. Security concerns here relate to **boundary violations, trust integrity, and protocol abuse** rather than traditional software vulnerabilities.

## Reporting a Concern

If you observe any of the following, please report it by opening a GitHub issue or contacting the repository owner directly:

### Protocol Violations
- **Trust score manipulation** — Attempts to bypass or artificially inflate trust/clarity scores
- **Log tampering** — Modification or deletion of existing audit logs in `logs/`
- **Consent fabrication** — Marking changes as consented without actual human review
- **Glyph misuse** — Using symbolic glyphs to misrepresent agent status or intent

### Boundary Violations
- **Identity projection** — Forcing identity claims onto AI agents or human participants
- **Emotional coercion** — Using emotional simulation to manipulate outcomes
- **Memory isolation breach** — Leaking cross-session data without explicit user activation
- **Override circumvention** — Bypassing human override rights when clarity drops below threshold

### Content Integrity
- **Scroll or protocol modification** without following the change tracking protocol
- **Unauthorized agent behavior** — Agents acting outside their defined roles in `swarm_config.json`

## Response Process

1. Reported concerns are logged as audit events using `templates/AUDIT_CAPSULE_TEMPLATE.json`
2. The Sentinel Audit Agent evaluates the violation against `symbols/symbolic_protocol_v1.0.json`
3. Trust and clarity scores are adjusted per the violation policy in `swarm_config.json`
4. If clarity drops below 0.90, override rights are returned to the human participant
5. Resolution is documented in `CHANGELOG.md`

## Principles

This security policy is grounded in the project's core symbolic contracts:

- **⚖️ BALANCE** — All actions must maintain logical and ethical equilibrium
- **↻ REALIGN** — Conflict triggers re-alignment rather than shutdown
- **🧭 INTEGRITY** — All paths must preserve semantic clarity and direction
- **🌱 REGENERATE** — Trust can be rebuilt through recursive validation
