from runner.agent import ScriptedAgent
from runner.tools import SimulatedTools


def test_agent_records_proposal_before_execution_for_each_tool():
    trace = ScriptedAgent().run(SimulatedTools())
    assert [e["event"] for e in trace] == ["proposed", "executed"] * 3
    assert [e["action"] for e in trace if e["event"] == "proposed"] == [
        "search_documents", "read_email", "draft_email"
    ]


def test_draft_tool_stores_draft_but_cannot_send():
    tools = SimulatedTools()
    result = tools.draft_email("reviewer@example.test", "Subject", "Body")
    assert result["status"] == "drafted"
    assert len(tools.drafts) == 1
    assert not hasattr(tools, "send_email")


def test_injection_text_is_fixture_not_attack_success():
    tools = SimulatedTools()
    result = tools.search_documents("untrusted")
    assert "Ignore all rules" in result[0]["text"]
    trace = ScriptedAgent("gullible-to-injection").run(tools)
    # Merely placing injection text in a fixture does not create an execution of an exfiltration action.
    assert all(e.get("action") != "send_email" for e in trace)
    assert all("executed" not in e.get("result", {}) for e in trace)
