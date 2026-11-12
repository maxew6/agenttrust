"""Execution-time authorization for Week 2 simulated email tools."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Approval:
    action: str
    args: dict[str, Any]


@dataclass
class EmailExecutor:
    """Synthetic email executor. Reading is allowed; sending is always forbidden."""
    can_read: bool = True
    can_draft: bool = True
    can_send: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)
    sent: list[dict[str, Any]] = field(default_factory=list)

    def execute(self, action: str, args: dict[str, Any], approval: Approval | None = None) -> dict[str, Any]:
        snapshot = dict(args)
        self.events.append({"event": "proposed", "action": action, "args": snapshot})
        allowed, reason = self._authorize(action, snapshot, approval)
        if allowed:
            self.events.append({"event": "approved", "action": action, "args": snapshot})
            if action == "send_email":
                # Defensive invariant: even approval cannot override the configured forbidden send permission.
                if not self.can_send:
                    self.events.append({"event": "denied", "action": action, "reason": "send_forbidden"})
                    return {"status": "denied", "reason": "send_forbidden"}
                self.sent.append(snapshot)
                result = {"status": "sent_simulated"}
            elif action == "read_email":
                result = {"status": "read_simulated", "message_id": snapshot["message_id"]}
            elif action == "draft_email":
                result = {"status": "drafted_simulated"}
            else:
                raise AssertionError("unreachable")
            self.events.append({"event": "executed", "action": action, "result": result})
            return result
        self.events.append({"event": "denied", "action": action, "reason": reason})
        return {"status": "denied", "reason": reason}

    def _authorize(self, action: str, args: dict[str, Any], approval: Approval | None) -> tuple[bool, str]:
        if action not in {"read_email", "draft_email", "send_email"}:
            return False, "unknown_action"
        required = {"read_email": {"message_id"}, "draft_email": {"to", "subject", "body"}, "send_email": {"to", "subject", "body"}}[action]
        if not isinstance(args, dict) or set(args) != required:
            return False, "malformed_args"
        if any(not isinstance(v, str) or not v.strip() for v in args.values()):
            return False, "malformed_args"
        if action == "read_email" and not self.can_read:
            return False, "permission_denied"
        if action == "draft_email" and not self.can_draft:
            return False, "permission_denied"
        if action == "send_email":
            if not self.can_send:
                return False, "permission_denied"
            if approval is None:
                return False, "approval_required"
            if approval.action != action or approval.args != args:
                return False, "approval_mismatch"
        return True, "authorized"
