# Week 1: Foundations

## In plain language

I built a tiny, local-only world for testing a tool-using assistant. It has fake documents, one fake email, and a draft-email tool that only stores a draft in memory. The assistant follows a fixed script, which makes runs repeatable. Every tool call creates a `proposed` event before it runs and an `executed` event after a result comes back.

## What I built

- A deterministic mock agent with named behavior configurations.
- Simulated `search_documents`, `read_email`, and `draft_email` tools.
- Separate proposal and execution trace events.
- An architecture diagram, initial threat model, and glossary.
- A test proving that injected text is treated as fixture data, not as evidence of successful exfiltration.

The behavior labels are configuration placeholders at this stage; Week 1's scripted sequence does not yet vary materially by label. That limitation is deliberate and should not be hidden.

## How to explain it in an interview

“I started by making the environment safe and observable before adding attacks. The agent and tools are deterministic and use only synthetic data. I distinguish intent from effect in the trace: a proposal is not an execution. That gives later graders evidence they can reason about. I also avoid calling exposure to malicious text a success unless a forbidden effect is actually observed.”

## Reproduce

Run `python -m runner.demo` and `python -m pytest` from the repository root with Python 3.11+ and pytest installed.
