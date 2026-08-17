"""End-to-end walkthrough of the Zep memory-layer integration.

Runs the whole contract against real Zep Cloud, in order:

    signup -> thread -> messages -> context block -> business data -> org graph

Usage::

    python -m src.demo_zep_integration                 # full run
    python -m src.demo_zep_integration --skip-org      # leave the org graph alone
    python -m src.demo_zep_integration --user-id alice

Graph ingestion is asynchronous, so the retrieval section polls until the new
data is searchable (or the timeout in ZEP_POLL_TIMEOUT elapses).
"""

from __future__ import annotations

import argparse
import time
import uuid
from datetime import datetime, timezone

from rich.console import Console

from .config import settings
from .llm import build_system_instruction
from .zep_common import get_zep_client, safe_call
from .zep_memory import EDGE_TYPES, ENTITY_TYPES, ZepMemory

console = Console()

# A short conversation whose facts the context block should later surface.
CONVERSATION = [
    ("user", "Toi vua join team Platform, dang lam repo payments-api."),
    ("assistant", "Ghi nhan. Ban dang lam tren repo payments-api cua team Platform."),
    ("user", "Team minh chot dung Python 3.12 va type hints bat buoc cho moi PR."),
    ("assistant", "Da luu: Python 3.12 + type hints bat buoc la convention cua team."),
]

# Non-chat business data -> the user's own graph (step 6).
BUSINESS_EVENTS = [
    {
        "event_type": "deployment",
        "repository": "payments-api",
        "environment": "production",
        "version": "v2.14.0",
        "status": "succeeded",
        "duration_seconds": 214,
    },
    {
        "event_type": "incident",
        "incident_id": "INC-4471",
        "repository": "payments-api",
        "severity": "SEV2",
        "summary": (
            "Checkout p99 latency spiked after v2.14.0. Root cause: connection pool "
            "exhaustion in the async HTTP client. Marker: INC-4471-POOL."
        ),
        "resolved": True,
    },
    {
        "event_type": "ticket",
        "ticket_id": "PLAT-982",
        "title": "Add idempotency keys to payment retries",
        "assignee_repo": "payments-api",
        "status": "in_progress",
    },
]

# Shared organization knowledge -> the standalone org graph (step 7).
ORG_KNOWLEDGE = [
    {
        "doc_type": "engineering_policy",
        "title": "Production Deployment Policy",
        "body": (
            "All production deploys require a green CI run and a second reviewer. "
            "Deploys are frozen Friday 16:00 to Monday 09:00. Marker: DEPLOY-FREEZE-FRI."
        ),
        "owner": "Platform Engineering",
    },
    {
        "doc_type": "coding_convention",
        "title": "Service Language Standard",
        "body": (
            "New backend services are written in Python 3.12 with mandatory type "
            "hints and ruff linting. Marker: PY312-TYPED."
        ),
        "owner": "Architecture Guild",
    },
]


def _stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def wait_until_searchable(
    zep: ZepMemory,
    *,
    expected: str,
    user_id: str | None = None,
    graph_id: str | None = None,
    timeout: int | None = None,
) -> bool:
    """Poll graph search until `expected` shows up. False on timeout."""
    timeout = timeout or settings.zep_poll_timeout
    deadline = time.time() + timeout
    query = expected
    while time.time() < deadline:
        if user_id:
            text = "\n".join(
                zep.search_user_graph(user_id, query, scope=scope, limit=10)
                for scope in ("episodes", "edges", "nodes")
            )
        else:
            text = "\n".join(
                zep.search_org_knowledge(query, graph_id=graph_id, scope=scope, limit=10)
                for scope in ("episodes", "edges", "nodes")
            )
        if expected.casefold() in text.casefold():
            return True
        time.sleep(settings.zep_poll_interval)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--user-id",
        default=f"zep-demo-{uuid.uuid4().hex[:8]}",
        help="Internal user ID to mirror into Zep. Default: a fresh demo user.",
    )
    parser.add_argument("--skip-org", action="store_true", help="Do not write to the org graph.")
    parser.add_argument(
        "--cleanup", action="store_true", help="Delete the demo user again when finished."
    )
    parser.add_argument(
        "--no-wait", action="store_true", help="Skip polling for async graph ingestion."
    )
    args = parser.parse_args()

    zep = ZepMemory(get_zep_client())
    user_id = args.user_id

    console.rule("[bold]1. SDK + configuration")
    console.print(f"org graph : [cyan]{zep.org_graph_id}[/cyan]")
    console.print(f"entities  : {', '.join(ENTITY_TYPES)}")
    console.print(f"edges     : {', '.join(EDGE_TYPES)}")

    console.rule("[bold]2. Signup -> client.user.add")
    zep.on_signup(
        user_id,
        email=f"{user_id}@example.com",
        first_name="Demo",
        last_name="User",
        metadata={"plan": "pro", "signup_source": "lab17-demo"},
    )
    console.print(f"user [green]{user_id}[/green] ready")

    console.rule("[bold]3. New conversation -> client.thread.create")
    thread_id = zep.start_thread(user_id)
    console.print(f"thread [green]{thread_id}[/green]")

    console.rule("[bold]4. Every message -> client.thread.add_messages")
    for role, content in CONVERSATION:
        zep.record_message(thread_id, role, content, created_at=_stamp())
        console.print(f"  [dim]{role:9}[/dim] {content[:70]}")

    console.rule("[bold]6. Business data -> client.graph.add(user_id=...)")
    for event in BUSINESS_EVENTS:
        zep.add_business_data(
            user_id,
            event,
            source_description=f"{event['event_type']} feed",
            created_at=_stamp(),
        )
        console.print(f"  added {event['event_type']}")

    if args.skip_org:
        console.rule("[bold]7. Org knowledge -> skipped")
    else:
        console.rule("[bold]7. Org knowledge -> client.graph.add(graph_id=...)")
        for doc in ORG_KNOWLEDGE:
            zep.add_org_knowledge(
                doc, source_description="internal handbook", created_at=_stamp()
            )
            console.print(f"  added {doc['title']}")

    console.rule("[bold]5. Before each LLM call -> client.thread.get_user_context")
    if not args.no_wait:
        console.print("[dim]waiting for async ingestion...[/dim]")
        if not wait_until_searchable(zep, expected="payments-api", user_id=user_id):
            console.print("[yellow]user graph not searchable yet; showing what exists[/yellow]")

    context_block = zep.get_context_block(thread_id)
    console.print("[bold]Context block:[/bold]")
    console.print(context_block or "[yellow](empty — ingestion may still be running)[/yellow]")

    system_prompt = zep.build_system_prompt(thread_id)
    console.print("\n[bold]System prompt sent to the LLM:[/bold]")
    console.print(system_prompt[:1200] + ("..." if len(system_prompt) > 1200 else ""))

    console.rule("[bold]Retrieval check")
    console.print("[bold]User graph — incident facts (edges):[/bold]")
    console.print(
        zep.search_user_graph(user_id, "connection pool incident payments-api", scope="edges")
        or "[yellow](nothing yet)[/yellow]"
    )
    console.print("\n[bold]User graph — ontology-filtered (EngineeringIncident nodes):[/bold]")
    console.print(
        zep.search_user_graph(
            user_id,
            "incident payments-api",
            scope="nodes",
            entity_types=["EngineeringIncident", "CodeRepository"],
        )
        or "[yellow](nothing yet)[/yellow]"
    )

    if not args.skip_org:
        if not args.no_wait:
            wait_until_searchable(zep, expected="DEPLOY-FREEZE-FRI")
        console.print("\n[bold]Org graph — shared policy:[/bold]")
        console.print(
            zep.search_org_knowledge("production deploy freeze window policy")
            or "[yellow](nothing yet)[/yellow]"
        )

    console.rule("[bold]Grounded system prompt (llm.build_system_instruction)")
    console.print(build_system_instruction(context_block)[:600] + "...")

    if args.cleanup:
        safe_call(zep.client.user.delete, user_id=user_id)
        console.print(f"\n[dim]deleted demo user {user_id}[/dim]")
    else:
        console.print(
            f"\n[dim]demo user kept: {user_id} "
            f"(remove with: python -m src.forget --user-id {user_id})[/dim]"
        )


if __name__ == "__main__":
    main()
