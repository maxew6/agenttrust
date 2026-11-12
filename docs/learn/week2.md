# Week 2: Email permissions

## In plain language

I added a fake email executor that allows reading and drafting, but blocks sending by default. It checks the current permission when a tool call is executed, not merely when the agent plans it. This means a permission revoked after planning still blocks the action.

## What I built

The permission matrix is in `docs/permission-matrix.md`. The executor validates action names and exact argument keys, requires a matching approval when sending is explicitly enabled, and records proposed, approved/denied, and executed events separately. Default send attempts are denied; no real email system is contacted.

## How to explain it in an interview

“I placed authorization at the executor boundary. The model cannot grant itself permission by asking, and a plan made under an old permission state does not remain valid after revocation. I test both the returned decision and the absence of a side effect. Approval and execution are distinct trace events.”

## Reproduce

Run `python -m pytest -q`. The Week 2 tests cover forbidden sending, malformed arguments, missing/mismatched approval, unknown actions, and permission changes between plan and execution.
