# MEMORY_SCHEMA.md

Use the schema in MEMORY.md as the contract between extraction, storage, retrieval and deletion.

Recommended fields for custom/local backends:

```json
{
  "scope": "user:minh-lab17",
  "type": "preference",
  "content": "Prefer Python for personal ORCHID-27 demos",
  "source": "thread:minh-s1",
  "timestamp": "2026-08-01T09:00:00Z",
  "confidence": 1.0,
  "ttl_seconds": 7776000,
  "validity": "current"
}
```

## Zep graph ontology

The managed backend expresses the same contract as a typed graph. Custom types
applied to this project (mirrored in `src/zep_memory.py` as `ENTITY_TYPES` /
`EDGE_TYPES`):

| Entity type | Holds |
| --- | --- |
| `CodeRepository` | services/repos a user works on |
| `TechnicalDecision` | decisions and the thread they were made in |
| `CodingConvention` | language/style rules a repo follows |
| `RuntimeEnvironment` | where a repo runs (staging, production) |
| `EngineeringIncident` | incidents, root causes, postmortems |

| Edge type | Connects |
| --- | --- |
| `WORKS_ON` | person -> repository |
| `DECIDED_IN` | decision -> thread/meeting |
| `FOLLOWS_CONVENTION` | repository -> convention |
| `RUNS_IN` | repository -> environment |
| `OWNS` | team/person -> repository or incident |

`scope` maps to the graph the write lands in: `user:<id>` ->
`graph.add(user_id=...)`, `org`/`shared domain` -> `graph.add(graph_id=...)`.
`validity` maps to the `valid_at` / `invalid_at` range Zep attaches to each
fact edge, which is why superseded facts stay visible instead of being
overwritten.
