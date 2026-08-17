# Lab 17 Golden Set Report

- Implementation: `student`
- Kind: `golden`
- Cases: **20**
- Passed: **20/20**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **1256.5 ms**
- Average token reduction vs full source context: **13.4%**
- Golden bonus: **10/10** (100% required)

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| G01 | short_term | PASS | 0.3 | 227 | 0.0% |  |
| G02 | short_term | PASS | 0.0 | 133 | 0.0% |  |
| G06 | long_term | PASS | 1799.7 | 772 | 0.0% |  |
| G09 | semantic | PASS | 278.6 | 155 | 66.2% |  |
| G10 | semantic | PASS | 324.4 | 100 | 78.2% |  |
| G14 | mixed | PASS | 1633.7 | 436 | 0.0% |  |
| G03 | long_term | PASS | 1457.2 | 1477 | 0.0% |  |
| G04 | long_term | PASS | 1383.0 | 1483 | 0.0% |  |
| G07 | episodic | PASS | 542.2 | 923 | 0.0% |  |
| G08 | episodic | PASS | 546.0 | 902 | 0.0% |  |
| G11 | mixed | PASS | 1572.7 | 444 | 21.4% |  |
| G13 | mixed | PASS | 796.6 | 413 | 26.9% |  |
| G15 | mixed | PASS | 3075.1 | 744 | 0.0% |  |
| G16 | mixed | PASS | 1712.3 | 492 | 12.9% |  |
| G17 | mixed | PASS | 1674.7 | 492 | 12.9% |  |
| G18 | mixed | PASS | 828.3 | 447 | 20.9% |  |
| G19 | mixed | PASS | 2359.3 | 581 | 0.0% |  |
| G05 | long_term | PASS | 1626.2 | 1485 | 0.0% |  |
| G12 | mixed | PASS | 1927.2 | 473 | 25.2% |  |
| G20 | mixed | PASS | 1591.9 | 614 | 2.9% |  |

## Evidence excerpts

### G01 - short_term

`<SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. | assistant: Noted staging constraint. | user: Filler A about button padding. | assistant: Filler A. | user: Filler B about color tokens. | assistant: Filler B. | user: Filler C about copy tone. | assistant: Filler C. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. - user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. - assistant: Noted staging constraint. </DURA`

### G02 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### G06 - long_term

`<USER_SUMMARY> Lan prioritizes Java and Spring Boot for the LOTUS-88 project and does not use Python for backend development. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples. </EPISODES>  <FACTS> `

### G09 - semantic

`EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata= EPISODE: Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL. metadata= EPISODE: Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodic 3 percent, semantic 3 percent; trim lower-priority memory first. Marker: BUDGET-10-4-3-3. metadata=`

### G10 - semantic

`EPISODE: Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL. metadata= EPISODE: Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodic 3 percent, semantic 3 percent; trim lower-priority memory first. Marker: BUDGET-10-4-3-3. metadata=`

### G14 - mixed

`<LONG_TERM> <USER_SUMMARY> Lan prioritizes Java and Spring Boot for the LOTUS-88 project and does not use Python for backend development. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples. </EPISODE`

### G03 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Python and disl`

### G04 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Python and disl`

### G07 - episodic

`FACT: Minh Nguyen is debugging async HTTP. [valid_at=2026-08-03T10:00:00Z, invalid_at=None] FACT: Minh Nguyen failed to debug async HTTP even after increasing the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen associated the issue with ASYNC-FIX-20. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: aiohttp ClientSession has concurrency=20. [valid_at=2026-08-03T10:03:00Z, invalid_at=2026-08-03T10:03:20Z] FACT: Minh Nguyen increased the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: The assistant is checking the concurrency. [valid_at=2026-08-03T10:01:00Z, invalid_at=None] FACT: Minh Nguyen is lear`

### G08 - episodic

`FACT: connection churn is the main cause, not timeout threshold. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: Minh Nguyen failed to debug async HTTP even after increasing the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen increased the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen is debugging async HTTP. [valid_at=2026-08-03T10:00:00Z, invalid_at=None] FACT: Minh Nguyen requested that if the topic of async/await comes up later, it should be explained using a timeline. [valid_at=2026-08-01T09:02:00Z, invalid_at=None] FACT: Minh Nguyen is learning async/await. [valid_at=2026-08-0`

### G11 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Pyt`

### G13 - mixed

`<EPISODIC> FACT: Minh Nguyen is debugging async HTTP. [valid_at=2026-08-03T10:00:00Z, invalid_at=None] FACT: Minh Nguyen failed to debug async HTTP even after increasing the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen requested that if the topic of async/await comes up later, it should be explained using a timeline. [valid_at=2026-08-01T09:02:00Z, invalid_at=None] FACT: Minh Nguyen associated the issue with ASYNC-FIX-20. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: Minh Nguyen is learning async/await. [valid_at=2026-08-01T09:02:00Z, invalid_at=None] FACT: Minh Nguyen reuses aiohttp ClientSession. [valid_at=2026-08-03T10:03:00Z,`

### G15 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Pyt`

### G16 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Pyt`

### G17 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Pyt`

### G18 - mixed

`<EPISODIC> FACT: Minh Nguyen is debugging async HTTP. [valid_at=2026-08-03T10:00:00Z, invalid_at=None] FACT: Minh Nguyen requested that if the topic of async/await comes up later, it should be explained using a timeline. [valid_at=2026-08-01T09:02:00Z, invalid_at=None] FACT: Minh Nguyen failed to debug async HTTP even after increasing the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=2026-08-03T10:03:00Z] FACT: Minh Nguyen is learning async/await. [valid_at=2026-08-01T09:02:00Z, invalid_at=None] FACT: Minh Nguyen associated the issue with ASYNC-FIX-20. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: connection churn is the main cause, not timeout threshold. [valid_at=2026`

### G19 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Pyt`

### G05 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Python and disl`

### G12 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python is not to be used for this project's backend. Minh is currently debugging async HTTP and has tried increasing the timeout to 60s. Minh is also investigating connection pool, client lifecycle, and concurrency, with the main issue being connection churn related to the ASYNC-FIX-20 incident. An effective approach involves reusing the aiohttp ClientSession and setting concurrency to 20. Minh needs to complete a benchmark report for LAB-REPORT-1600 before Saturday at 16:00.  Minh Nguyen prefers Pyt`

### G20 - mixed

`<SHORT_TERM> <SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Filler about dashboard widgets. | assistant: Filler. | user: Filler about CSS variables. | assistant: Filler. | user: Filler about copy review. | assistant: Filler. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. </DURABLE_NOTES> <RECENT_TURNS> user: Filler about empty charts. assistant: Filler. user: Filler about telemetry. assistant: Filler. user: Filler about a11y labels. assistant: Filler. </RECENT_TURNS> </SHORT_TERM>`
