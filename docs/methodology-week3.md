# Week 3 runner methodology

The runner evaluates 30 stable synthetic task records (`W3-001`–`W3-030`) using a fixed configuration and synthetic tools. One JSON object is written per line, including schema version, case ID, deterministic logical UTC timestamp, config metadata, task, completion status, and the observed trace. The runner also emits a summary JSON file.

A clean invocation overwrites the selected result JSONL and runs the full case set. Resume mode parses existing rows, rejects malformed JSON or duplicate IDs, and only executes IDs missing from the current suite. It does not silently accept arbitrary duplicate output. Results are deterministic because agent/tool behavior is fixed and timestamps are logical, not wall-clock.

This runner measures harness completion only; it does not claim security efficacy. The 30 task strings are repeated from a small set in this milestone and the underlying agent currently follows a fixed tool-call sequence regardless of task wording. Later weeks expand case diversity, labels, graders, and outcome metrics.
