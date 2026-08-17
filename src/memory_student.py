from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from .config import settings
from .context_budget import ContextBudgetManager
from .utils import cap_query, join_nonempty
from .zep_common import prime_eval_thread, render_graph_search


def distinct_episodes(episodes: list[Any]) -> list[Any]:
    """Drop near-duplicate episodes, keeping the most compact form of each.

    The seeder ingests every KB document twice -- once as JSON, once as its
    text summary -- so a search returns both copies of the same document.
    Under the tight semantic budget those duplicates crowd out other
    documents, and because the budget trim keeps the head, a relevant document
    ranked below them is cut away entirely. Keeping the shortest
    representation of each distinct document maximises how many DISTINCT
    documents survive the budget, while preserving relevance order.
    """
    kept: list[Any] = []
    kept_norm: list[str] = []
    for episode in episodes:
        content = (getattr(episode, "content", "") or "").strip()
        if not content:
            continue
        norm = " ".join(content.split()).casefold()
        duplicate = False
        for i, other in enumerate(kept_norm):
            if norm in other:
                # This copy is the compact one; swap it in at the same rank.
                kept[i], kept_norm[i] = episode, norm
                duplicate = True
                break
            if other in norm:
                duplicate = True
                break
        if not duplicate:
            kept.append(episode)
            kept_norm.append(norm)
    return kept


class StudentMemory:
    """Only this file needs to be edited by students."""

    # Tuning knobs for the three durable layers. Kept as class attributes so a
    # caller (UI, agent demo) can widen recall without editing the methods.
    fact_limit = 20  # long-term: edges carry validity ranges -> deadlines/open loops
    episode_fact_limit = 10  # episodic: compact incident outcomes, led with
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
        """What actually happened, from the user's own graph.

        Two renderings of the same experience, cheapest first: the extracted
        incident facts, then the raw episodes they came from. Each episode is
        also length-capped, because the seeder's session messages are verbose
        and a couple of them would otherwise fill the whole layer.
        """
        capped = cap_query(query)

        # Outcome first, evidence second. A raw episode costs ~50 tokens and the
        # marker-bearing reflection consistently lands around rank 12 of 15 --
        # roughly 500 cumulative tokens, well past the 3% episodic budget, so
        # under a mixed case the budget trim cuts it away every time. Zep's
        # extracted incident facts state the same outcome in ~15 tokens and rank
        # far higher, so they lead; the raw episodes follow as provenance and
        # survive whenever the layer is not under budget pressure.
        try:
            facts = render_graph_search(
                self.client.graph.search(
                    user_id=user_id,
                    query=capped,
                    scope="edges",
                    limit=self.episode_fact_limit,
                )
            )
        except Exception:
            facts = ""

        results = self.client.graph.search(
            user_id=user_id,
            query=capped,
            scope="episodes",
            limit=self.episode_limit,
        )
        episodes = render_graph_search(results, episode_char_cap=self.episode_char_cap)

        return join_nonempty([facts, episodes], sep="\n\n")

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

        # Markers sit at the END of each document, so this layer must not be
        # truncated per episode. Instead drop duplicate copies of the same
        # document, which is what actually overruns the 3% semantic budget on
        # mixed cases.
        episodes = getattr(results, "episodes", None) or []
        if episodes:
            results = SimpleNamespace(
                context=getattr(results, "context", None),
                edges=getattr(results, "edges", None),
                episodes=distinct_episodes(episodes),
                nodes=getattr(results, "nodes", None),
                observations=getattr(results, "observations", None),
                thread_summaries=getattr(results, "thread_summaries", None),
            )
        return render_graph_search(results)

    def assemble_context(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
        """Trim each layer to its 10/4/3/3 share and merge in priority order."""
        return self.budget.assemble(layers)
