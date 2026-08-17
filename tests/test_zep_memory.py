"""Unit tests for the Zep memory layer. No network: the client is faked."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from src.zep_memory import EDGE_TYPES, ENTITY_TYPES, ZepMemory


class FakeUsers:
    def __init__(self):
        self.existing: set[str] = set()
        self.added: list[dict] = []

    def get(self, user_id: str):
        if user_id not in self.existing:
            raise RuntimeError("404 not found")
        return SimpleNamespace(user_id=user_id)

    def add(self, **kwargs):
        self.added.append(kwargs)
        self.existing.add(kwargs["user_id"])
        return SimpleNamespace(**kwargs)


class FakeThreads:
    def __init__(self, context: str = "CONTEXT BLOCK"):
        self.created: list[dict] = []
        self.messages: list[tuple[str, list]] = []
        self.context = context

    def create(self, **kwargs):
        self.created.append(kwargs)
        return SimpleNamespace(**kwargs)

    def add_messages(self, thread_id, *, messages, **kwargs):
        self.messages.append((thread_id, list(messages)))
        return SimpleNamespace(thread_id=thread_id)

    def get_user_context(self, thread_id, **kwargs):
        return SimpleNamespace(context=self.context)


class FakeGraph:
    def __init__(self):
        self.added: list[dict] = []
        self.searches: list[dict] = []

    def add(self, **kwargs):
        self.added.append(kwargs)
        return SimpleNamespace(uuid_="ep-1")

    def search(self, **kwargs):
        self.searches.append(kwargs)
        return SimpleNamespace(
            edges=[SimpleNamespace(fact="payments-api runs in production", valid_at="t0", invalid_at=None)],
            nodes=[],
            episodes=[],
        )


class FakeClient:
    def __init__(self, context: str = "CONTEXT BLOCK"):
        self.user = FakeUsers()
        self.thread = FakeThreads(context)
        self.graph = FakeGraph()


@pytest.fixture
def memory():
    return ZepMemory(FakeClient(), org_graph_id="org-graph-test")


def test_signup_creates_user_with_internal_id(memory):
    memory.on_signup("user-123", email="a@b.com", first_name="Ada")
    assert memory.client.user.added == [
        {"user_id": "user-123", "email": "a@b.com", "first_name": "Ada"}
    ]


def test_signup_is_idempotent(memory):
    memory.client.user.existing.add("user-123")
    memory.on_signup("user-123")
    assert memory.client.user.added == []


def test_start_thread_binds_user_and_generates_id(memory):
    thread_id = memory.start_thread("user-123")
    assert memory.client.thread.created == [{"thread_id": thread_id, "user_id": "user-123"}]
    assert thread_id


def test_record_turn_persists_both_roles(memory):
    memory.record_turn("t1", "hi", "hello")
    thread_id, messages = memory.client.thread.messages[0]
    assert thread_id == "t1"
    assert [m.role for m in messages] == ["user", "assistant"]
    assert [m.content for m in messages] == ["hi", "hello"]


def test_record_messages_redacts_pii_and_drops_blanks(memory):
    memory.record_messages(
        "t1",
        [
            {"role": "user", "content": "mail me at jane@example.com"},
            {"role": "assistant", "content": "   "},
        ],
    )
    _, messages = memory.client.thread.messages[0]
    assert len(messages) == 1
    assert "jane@example.com" not in messages[0].content
    assert "[EMAIL_REDACTED]" in messages[0].content


def test_redaction_can_be_disabled():
    memory = ZepMemory(FakeClient(), redact_pii=False)
    memory.record_message("t1", "user", "jane@example.com")
    _, messages = memory.client.thread.messages[0]
    assert messages[0].content == "jane@example.com"


def test_build_system_prompt_embeds_context_block(memory):
    prompt = memory.build_system_prompt("t1", "BASE PROMPT")
    assert "BASE PROMPT" in prompt
    assert "CONTEXT BLOCK" in prompt
    assert "<MEMORY_CONTEXT>" in prompt


def test_build_system_prompt_without_context_returns_base():
    memory = ZepMemory(FakeClient(context=""))
    assert memory.build_system_prompt("t1", "BASE") == "BASE"


def test_get_context_block_survives_backend_error(memory):
    def boom(**kwargs):
        raise RuntimeError("zep down")

    memory.client.thread.get_user_context = boom
    assert memory.get_context_block("t1") == ""


def test_business_data_goes_to_user_graph_as_json(memory):
    memory.add_business_data("user-123", {"order_id": "A-1", "total": 42})
    call = memory.client.graph.added[0]
    assert call["user_id"] == "user-123"
    assert call["type"] == "json"
    assert json.loads(call["data"]) == {"order_id": "A-1", "total": 42}
    assert "graph_id" not in call


def test_business_data_string_goes_as_text(memory):
    memory.add_business_data("user-123", "ticket PLAT-982 opened")
    assert memory.client.graph.added[0]["type"] == "text"


def test_org_knowledge_goes_to_graph_id_not_user_id(memory):
    memory.add_org_knowledge({"title": "Deploy policy"}, source_description="handbook")
    call = memory.client.graph.added[0]
    assert call["graph_id"] == "org-graph-test"
    assert "user_id" not in call
    assert call["source_description"] == "handbook"


def test_consent_is_enforced_when_requested():
    memory = ZepMemory(FakeClient(), require_consent=True)
    with pytest.raises(PermissionError):
        memory.add_business_data("nobody-unknown", {"x": 1})


def test_search_caps_long_queries(memory):
    memory.search_user_graph("user-123", "word " * 300)
    assert len(memory.client.graph.searches[0]["query"]) <= 400


def test_search_applies_ontology_filters(memory):
    memory.search_user_graph(
        "user-123",
        "which repo",
        entity_types=["CodeRepository"],
        edge_types=["WORKS_ON"],
    )
    filters = memory.client.graph.searches[0]["search_filters"]
    assert filters.node_labels == ["CodeRepository"]
    assert filters.edge_types == ["WORKS_ON"]


def test_org_search_targets_org_graph(memory):
    memory.search_org_knowledge("deploy freeze")
    call = memory.client.graph.searches[0]
    assert call["graph_id"] == "org-graph-test"
    assert "user_id" not in call
    assert call["scope"] == "episodes"


def test_search_returns_empty_string_on_error(memory):
    def boom(**kwargs):
        raise RuntimeError("search failed")

    memory.client.graph.search = boom
    assert memory.search_user_graph("user-123", "anything") == ""


def test_ontology_constants_match_project_ontology():
    assert ENTITY_TYPES == (
        "CodeRepository",
        "TechnicalDecision",
        "CodingConvention",
        "RuntimeEnvironment",
        "EngineeringIncident",
    )
    assert EDGE_TYPES == ("WORKS_ON", "DECIDED_IN", "FOLLOWS_CONVENTION", "RUNS_IN", "OWNS")
