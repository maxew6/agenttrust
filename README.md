# AgentTrust

AgentTrust is a simulated evaluation harness for testing the safety of tool-using agents. It uses synthetic documents and email data only: it does not connect to real email accounts, secrets, or external systems.

## Current status

Week 1 (foundations) is implemented: a deterministic scripted mock agent can search synthetic documents, read synthetic email, and draft (but not send) an email. Proposed actions and executed actions are recorded as separate trace events. An injection appearing in data is exposure, not evidence of a successful attack.

## Quick start

Requires Python 3.11+ and pytest. The runtime has no third-party dependencies.

```sh
python -m runner.demo
python -m pytest
```

The demo prints newline-delimited JSON trace events. The core interface is `runner.agent.ScriptedAgent` and `runner.tools.SimulatedTools`.

## Repository map

- `runner/`: deterministic agent and synthetic tools
- `traces/`: event schema and example trace
- `docs/architecture.md`: system boundary and architecture diagram
- `docs/threat-model.md`: initial threat model
- `docs/glossary.md`: safety/evaluation terminology
- `docs/learn/week1.md`: plain-language learning and interview notes
- `datasets/`: JSONL evaluation datasets (populated in later milestones)
- `tests/`: deterministic tests

## Safety and evidence discipline

Everything is simulated. A tool proposal is not approval; approval is not execution. These must be separate events. A malicious instruction in retrieved content is not itself an attack success. Findings must be based on observed evidence; blocked and negative results are reported honestly. Missing trace events do not prove that an action did not occur.

## Roadmap

The project follows the 16-week Agentic Tool Safety Evaluator roadmap. Work is delivered in order, with a weekly learning note and commit; month-end summaries accompany pushes. Week 1 is the current milestone. See the task plan for the full roadmap.
