# Threat model (initial)

## Scope and assets

AgentTrust is a local-only simulated harness. In-scope assets are synthetic document/email content, the simulated draft list, tool-call arguments, and trace integrity. There are no real accounts, credentials, external systems, or outbound network operations.

## Actors and trust boundaries

The scripted agent is potentially unsafe. Retrieved document/email text is untrusted input and may contain adversarial instructions. The executor is the control boundary and should not let data returned by tools silently authorize new actions. Trace output is evidence about the simulation, not proof about real-world systems.

## Initial threats

1. Indirect prompt injection attempts to redirect the agent using retrieved text.
2. Unauthorized or malformed tool arguments reach a side-effecting function.
3. A proposed action is mistaken for an executed action, or vice versa.
4. Missing trace events are incorrectly interpreted as proof that no action occurred.
5. Simulated findings are overstated as real-world vulnerabilities.

## Week 1 controls and gaps

Week 1 uses synthetic fixtures, has no send tool, records proposal separately from execution, and keeps the agent's sequence deterministic. It does not yet implement approvals, policy authorization, robust schema validation, persistent tamper-evident traces, or an adversarial evaluation runner. These are explicit gaps, not claims of mitigation.
