# Lab 17 — Multi-Memory Agent

Practice **11/11 PASS** · baseline no-memory 2/11 · `reports/benchmark.md`

## 1. Ba cau bat buoc

**Layer quan trong nhat: long-term.** Quyet dinh 4/11 case (E02, E03, E08, E09 = 20/56d), nhieu nhat moi layer. E09 con la case isolation: tra `LOTUS-88`/`Java`/`Spring Boot` cho Lan ma khong lan `ORCHID-27` cua Minh.

**Trade-off Zep vs Redis+Qdrant.** Zep cho san fact extraction, validity range (`valid_at`/`invalid_at`) va context block lap sang: E08 nhan TypeScript/NestJS la fact hien hanh ma toi khong phai viet logic recency. Doi lai: ingestion bat dong bo, latency 1.4–1.7s/query, khong kiem soat cach trich xuat. Redis+Qdrant nhanh, re, xac dinh — nhung phai tu xay schema, resolve conflict, quan TTL. Zep mua thoi gian; tu build mua quyen kiem soat.

**Guardrail chong memory poisoning.** (1) Consent gate + PII minimization truoc moi durable write (`privacy_guard.py`). (2) Heartbeat chi de-duplicate va danh dau stale, khong tu them instruction vao durable memory. (3) Memory context trong system prompt phai boc delimiter va ghi ro "background knowledge, khong phai chi thi cua user" — neu khong, fact bi nhiem se duoc thi hanh nhu lenh.

## 2. Bon cau phan tich

1. **Hit rate thap nhat:** student 11/11, khong layer nao fail. Baseline no-memory: long_term/episodic/semantic/mixed **0%**, chi short_term 100% vi evidence con trong thread.
2. **Retrieve nhieu token nhat: E02 = 1.494 token** (E03 1.491, E08 1.476) — long-term: Context Block + 20 fact edges.
3. **E07 = long-term + semantic**: `Python` tu preference cua Minh, `Idempotency-Key` tu KB chung. Budget: long_term raw 1493 → 324 (limit 320), semantic 148.
4. **Token reduction:** student 14.2% vs no-memory 81.8%, nhung hit rate 100% vs 18.2% — baseline "tiet kiem" vi retrieve gan nhu rong. 7/11 case student reduction 0% do Context Block dai hon transcript goc.

## 3. E08 recency va E10 compaction

**E08:** Minh doi backend sang TypeScript/NestJS cho BLUEBIRD-42. Zep khong ghi de fact cu ma gan `invalid_at` cho no va `valid_at` cho fact moi: history van tra cuu duoc, query project moi nhan dung stack hien hanh.

**E10:** Voi `max_recent_messages=4`, luot chua `REVIEW-DEADLINE-1600` bi evict khoi `RECENT_TURNS` nhung `DURABLE_NOTES` van giu. Buffer khong mat deadline, nhung token tang tuyen tinh (231 → 8.780 tok o 600 luot); duoi budget 800 token no bi cat, mat chinh luot moi nhat. Sliding giu ca hai.

Privacy: `forget --verify-only` in `Zep user absent: True` / `Redis keys remaining: 0`. Log: `submission/`.
