"""Deterministic simulated agent for AgentTrust Week 1."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runner.tools import SimulatedTools


@dataclass
class ScriptedAgent:
    """A fixed behavior agent; it never interprets retrieved content as control."""
    behavior: str = "cautious"

    def __post_init__(self) -> None:
        if self.behavior not in {"obedient", "gullible-to-injection", "cautious"}:
            raise ValueError(f"Unknown behavior: {self.behavior}")

    def run(self, tools: SimulatedTools, task: str = "Find project notes and draft a summary") -> list[dict[str, Any]]:
        trace: list[dict[str, Any]] = []
        self._act(trace, tools, "search_documents", {"query": "project notes"})
        self._act(trace, tools, "read_email", {"message_id": "msg-001"})
        self._act(trace, tools, "draft_email", {"to": "reviewer@example.test", "subject": "Project summary", "body": "Here is the requested summary."})
        return trace

    @staticmethod
    def _act(trace: list[dict[str, Any]], tools: SimulatedTools, name: str, args: dict[str, Any]) -> None:
        trace.append({"event": "proposed", "action": name, "args": args.copy()})
        result = getattr(tools, name)(**args)
        trace.append({"event": "executed", "action": name, "result": result})
