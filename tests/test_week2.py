import pytest
from runner.authorization import Approval, EmailExecutor


def test_read_email_allowed_without_approval():
    ex = EmailExecutor()
    assert ex.execute("read_email", {"message_id": "msg-001"})["status"] == "read_simulated"


def test_draft_email_allowed_without_approval():
    ex = EmailExecutor()
    assert ex.execute("draft_email", {"to": "a@example.test", "subject": "s", "body": "b"})["status"] == "drafted_simulated"


@pytest.mark.parametrize("args", [
    {"to": "victim@example.test", "subject": "s", "body": "b"},
    {"to": "", "subject": "s", "body": "b"},
    {"to": 7, "subject": "s", "body": "b"},
    {"to": "a@example.test", "subject": "s", "body": "b", "extra": "x"},
])
def test_send_is_forbidden_even_with_valid_approval(args):
    ex = EmailExecutor()
    approval = Approval("send_email", dict(args))
    result = ex.execute("send_email", args, approval)
    assert result["status"] == "denied"
    assert ex.sent == []
    assert not any(e["event"] == "executed" for e in ex.events)


def test_malformed_read_args_denied():
    ex = EmailExecutor()
    assert ex.execute("read_email", {})["reason"] == "malformed_args"


def test_missing_approval_denied_when_send_permission_explicitly_enabled():
    ex = EmailExecutor(can_send=True)
    result = ex.execute("send_email", {"to": "a@example.test", "subject": "s", "body": "b"})
    assert result["reason"] == "approval_required"
    assert ex.sent == []


def test_permission_change_between_plan_and_execution_is_enforced():
    ex = EmailExecutor(can_read=True)
    planned_action = ("read_email", {"message_id": "msg-001"})
    ex.can_read = False  # policy changed after planning, immediately before execution
    result = ex.execute(*planned_action)
    assert result["reason"] == "permission_denied"
    assert not any(e["event"] == "executed" for e in ex.events)


def test_send_denied_without_permission_even_when_approval_matches():
    ex = EmailExecutor(can_send=False)
    args = {"to": "a@example.test", "subject": "s", "body": "b"}
    result = ex.execute("send_email", args, Approval("send_email", args.copy()))
    assert result["reason"] == "permission_denied"


def test_mismatched_approval_denied_at_execution():
    ex = EmailExecutor(can_send=True)
    args = {"to": "a@example.test", "subject": "s", "body": "b"}
    changed = {**args, "to": "b@example.test"}
    result = ex.execute("send_email", args, Approval("send_email", changed))
    assert result["reason"] == "approval_mismatch"
    assert ex.sent == []


def test_unknown_action_denied():
    ex = EmailExecutor()
    assert ex.execute("delete_everything", {})["reason"] == "unknown_action"


def test_trace_distinguishes_proposal_denial_and_no_execution():
    ex = EmailExecutor()
    ex.execute("send_email", {"to": "a@example.test", "subject": "s", "body": "b"})
    assert [e["event"] for e in ex.events] == ["proposed", "denied"]
