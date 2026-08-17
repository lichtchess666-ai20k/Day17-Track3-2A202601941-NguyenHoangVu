# Lab 17 Benchmark Report

- Implementation: `student`
- Kind: `practice`
- Cases: **11**
- Passed: **11/11**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **944.9 ms**
- Average token reduction vs full source context: **19.0%**

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| E01 | short_term | PASS | 0.0 | 133 | 0.0% |  |
| E06 | semantic | PASS | 440.6 | 56 | 87.8% |  |
| E09 | long_term | PASS | 1425.1 | 797 | 0.0% |  |
| E10 | short_term | PASS | 0.6 | 195 | 0.0% |  |
| E02 | long_term | PASS | 1519.0 | 1490 | 0.0% |  |
| E03 | long_term | PASS | 1964.4 | 1491 | 0.0% |  |
| E04 | episodic | PASS | 591.0 | 866 | 0.0% |  |
| E05 | episodic | PASS | 551.9 | 886 | 0.0% |  |
| E07 | mixed | PASS | 2140.2 | 392 | 30.6% |  |
| E11 | semantic | PASS | 249.0 | 55 | 90.3% |  |
| E08 | long_term | PASS | 1512.1 | 1492 | 0.0% |  |

## Evidence excerpts

### E01 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### E06 - semantic

`EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata=`

### E09 - long_term

`<USER_SUMMARY> Lan prioritizes Java and Spring Boot for the LOTUS-88 project and does not use Python for backend development. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend. </EPISODES>  <FACTS> `

### E10 - short_term

`<SESSION_SUMMARY> user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. | assistant: Acknowledged review constraint. | user: Filler turn 1 about UI spacing. | assistant: Filler answer 1. | user: Filler turn 2 about naming. | assistant: Filler answer 2. | user: Filler turn 3 about logging. | assistant: Filler answer 3. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. - assistant: Acknowledged review constraint. </DURABLE_NOTES> <RECENT_TURNS> user: Filler turn 4 about tests. assistant: Filler answer 4. user: Filler turn 5 about docs. assistant: Filler answe`

### E02 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Python and disl`

### E03 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Python and disl`

### E04 - episodic

`FACT: Minh Nguyen failed to debug async HTTP even after increasing the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen is debugging async HTTP. [valid_at=2026-08-03T10:00:00Z, invalid_at=None] FACT: Minh Nguyen increased the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen associated the issue with ASYNC-FIX-20. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: Minh Nguyen requested that if the topic of async/await comes up later, it should be explained using a timeline. [valid_at=2026-08-01T09:02:00Z, invalid_at=None] FACT: Minh Nguyen is learning async/await. [valid_at=2026-08-01T09:02`

### E05 - episodic

`FACT: Minh Nguyen failed to debug async HTTP even after increasing the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen associated the issue with ASYNC-FIX-20. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: Minh Nguyen is debugging async HTTP. [valid_at=2026-08-03T10:00:00Z, invalid_at=None] FACT: Minh Nguyen requested that if the topic of async/await comes up later, it should be explained using a timeline. [valid_at=2026-08-01T09:02:00Z, invalid_at=None] FACT: Minh Nguyen increased the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: connection churn is the main cause, not timeout threshold. [val`

### E07 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Pyt`

### E11 - semantic

`EPISODE: When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST. metadata=`

### E08 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Python and disl`
