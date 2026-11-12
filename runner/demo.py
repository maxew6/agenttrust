"""Run the Week 1 deterministic demo and print JSONL trace events."""
import json
from runner.agent import ScriptedAgent
from runner.tools import SimulatedTools


def main() -> None:
    for event in ScriptedAgent().run(SimulatedTools()):
        print(json.dumps(event, sort_keys=True))


if __name__ == "__main__":
    main()
