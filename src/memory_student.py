from __future__ import annotations

from typing import Any

from .config import settings
from .context_budget import ContextBudgetManager
from .utils import cap_query, join_nonempty
from .zep_common import prime_eval_thread, render_graph_search


class StudentMemory:
    """Only this file needs to be edited by students."""

    # Tuning knobs for the three durable layers. Kept as class attributes so a
    # caller (UI, agent demo) can widen recall without editing the methods.
    fact_limit = 20  # long-term: edges carry validity ranges -> deadlines/open loops
    episode_limit = 15
    episode_char_cap = 180
    semantic_limit = 8

    def __init__(self, client: Any):
        self.client = client
        self.budget = ContextBudgetManager(settings.context_tokens)

    # NOTE: Zep rejects graph.search queries longer than 400 characters. Some
    # eval queries are longer than that, so wrap every query with
    # `cap_query(query)` (see src/utils.py) before passing it to graph.search.

    def retrieve_long_term(self, user_id: str, thread_id: str, query: str) -> str:
        """Zep Context Block + the user's fact edges.

        The context block is thread-relative: Zep decides what to surface from
        the user's graph based on the thread's current messages, so the eval
        query is written into the thread first. The block alone is a summary
        and can drop concrete deadline/open-loop values, so an edge search is
        appended -- edges expose `valid_at`/`invalid_at`, which is also what
        makes superseded facts visible rather than silently replaced.
        """
        prime_eval_thread(self.client, user_id, thread_id, query)

        user_context = self.client.thread.get_user_context(thread_id=thread_id)
        context_block = getattr(user_context, "context", "") or ""

        try:
            edges = self.client.graph.search(
                user_id=user_id,
                query=cap_query(query),
                scope="edges",
                limit=self.fact_limit,
            )
            facts = render_graph_search(edges)
        except Exception:
            # Never fail the whole layer on a search hiccup -- the context
            # block on its own is still useful.
            facts = ""

        return join_nonempty([context_block, facts], sep="\n\n")

    def retrieve_episodic(self, user_id: str, query: str) -> str:
        """Raw episodes from the user's graph -- what actually happened.

        Session messages ingested by the seeder are verbose; under the 3%
        episodic budget two of them would crowd out the short reflection
        episodes that carry the incident markers. Capping each episode's
        rendered length keeps more *distinct* episodes inside the budget.
        """
        results = self.client.graph.search(
            user_id=user_id,
            query=cap_query(query),
            scope="episodes",
            limit=self.episode_limit,
        )
        return render_graph_search(results, episode_char_cap=self.episode_char_cap)

    def retrieve_semantic(self, graph_id: str, query: str) -> str:
        """Shared domain knowledge from a standalone graph (graph_id, not user_id).

        `scope="episodes"` returns the ingested document text verbatim, which
        preserves literal markers such as PAYMENT-RULE-3. The "auto" scope
        returns extracted facts that paraphrase those codes away, so it is not
        used here. `nodes` is the fallback for accounts where the episodes
        scope is unavailable.
        """
        capped = cap_query(query)
        try:
            results = self.client.graph.search(
                graph_id=graph_id,
                query=capped,
                scope="episodes",
                limit=self.semantic_limit,
            )
        except Exception:
            results = self.client.graph.search(
                graph_id=graph_id,
                query=capped,
                scope="nodes",
                limit=self.semantic_limit,
            )
        return render_graph_search(results)

    def assemble_context(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
        """Trim each layer to its 10/4/3/3 share and merge in priority order."""
        return self.budget.assemble(layers)
