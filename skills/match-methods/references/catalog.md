# Candidate fields and family notes

Catalogs grow when research earns a row. These notes are not a closed menu and not automatic recommendations. Public figures below were visible on the cited pages on 11 Nov 2026. They are not measurements from this repository, and they do not transfer by default.

## Fields

| Field | What to record |
|---|---|
| Problem and mechanism | The failure it addresses, and how the process would change |
| Fit and anti-fit | Workload facts that support or contradict it |
| Prerequisites | Data, labels, index, interfaces, compute, and skills. A missing one is a separate proposal |
| Evidence | Source, conditions, whether the result was measured or only reported, uncertainty, and transfer limits |
| Tradeoffs | Quality, tail latency, throughput, usage, setup, and maintenance |
| Governance | Residency, privacy, abstention, fallback, and rollback |
| Composition | Stages it can sit beside, dependencies, interference, and where the bottleneck may move |
| Discriminating test | The cheapest observation here that could reject it |

## Families

**Identifiers versus paraphrase.** A code, title, or rare token is a reason to look at exact lookup, filters, or lexical retrieval. Lexical retrieval is not embedding search. A query that shares few terms with the source is a reason to look at dense or hybrid retrieval. Dense retrieval does not always win, including on identifiers. The [DPR anthology abstract](https://aclanthology.org/2020.emnlp-main.550/) reports that, on that paper's open-domain sets, a dense retriever beat a strong Lucene-BM25 baseline by 9%–19% absolute top-20 passage accuracy. That is the abstract's report. It is not a result for a new corpus.

**Neighbor text versus index-time context.** If the right document is in hand and the deciding table, definition, or exception sits nearby, investigate a capped query-time read of that neighbor. Do not default to loading the entire document. A graph is not required. Index-time contextual retrieval is a different method: [Anthropic's writeup](https://www.anthropic.com/research/contextual-retrieval) (the older news URL redirects here) describes prepending a short chunk-specific context, usually 50–100 tokens, before embedding and before BM25 indexing. On that page the vendor reports top-20 chunk failure falling from 5.7% to 2.9% with contextual embeddings plus contextual BM25, and to 1.9% after reranking. Those figures were not repeated here.

**Recall without a precise shortlist.** If the gold item is in a larger set but not in the window the model reads, investigate reranking or a tighter filter. A reranker cannot recover a document the first stage never retrieved.

**Cache versus freshness.** Reuse of a prompt prefix is not source freshness and not index invalidation. A long cache hit does not prove the underlying source is current. Vendor limits change. This note does not restate TTLs, prices, or a header version.

**What was sent.** Measure skill bodies and tool definitions actually sent. An installed catalog can be large while a request is small, or the reverse. Deferred loading, where a vendor documents it, is that vendor's method. It is not a general law. Omitting a tool the next turn needs is an anti-fit.

**Graphs after lean baselines fail.** A graph or ontology is in scope when a named relation across documents fails lean baselines such as another query, citation following, or a metadata join. Include extraction, index, and maintenance cost. Graph-by-default is an anti-fit for a single-document question. A public [GraphRAG post](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/) describes entity and community structure aimed at corpus-level questions. That description is not a controlled comparison for a new corpus.

**Wrong hop or a broken meter.** Missing official URLs or a misleading tool description often need a result shape or a loader change, not a new model alone. Empty metrics need instrumentation and a rubric fix. A retrieval change will not repair a measurement gap. If support checks reject a document that is already in hand, test paraphrase, parser loss, an exact but false quote, and a mislocated gate before any patch. If the problem is location, keep the source as a nonbinding lead, return original text through a stable span, and keep the support check. Do not disable it globally.

## Symptom measures

| Symptom | Look at first | It can separate |
|---|---|---|
| The task is slow while several workers run | End-to-end time, the delaying branch, queues, retries | A slow model, a slow tool, a necessary wait, or a saturated shared resource |
| The request looks large because many tools are installed | Definitions actually sent, repeats, cache use, selection quality | Catalog size versus a genuinely overloaded request |
| The same document is reread and evidence is rejected | Rejection reason, source text, new information per retry | Paraphrase, truncation, a false exact quote, or a mislocated gate |
| The answer is wrong after the document was found | Parser output, worker input, verifier input, persisted result | Retrieval versus context loss, interpretation, or a write-path bug |
| Adding workers makes the wait worse | Concurrency, rate limits, queue age, timeouts | A shared limit versus too little parallelism |
| People keep restarting the work | Stop reasons, handoffs, repeated investigation, waiting time | A necessary approval versus missing continuity |

## Bounded models and independent agents

Rules, existing classifiers, and small bounded calls come before a training proposal unless evidence already favors training. [TypeSafe's models page](https://docs.typesafe.ai/models), fetched 11 Nov 2026, described Jev 1.14.0 as available from 14 October 2026, with aliases that point at versioned ids, and said Jev is not fine-tuned or LoRA-adapted with customer data. [System One](https://docs.typesafe.ai/concepts/system-one) lists bounded primitives such as Choice and Score. That is a public candidate family, not a selected router, and not a role pin. Re-read the pages before relying on a version. Prices are intentionally not copied here.

The [A2A specification](https://a2a-protocol.org/latest/specification/), fetched the same day, is an interoperability protocol for independently deployed agents. In that text, Send Message may be idempotent and may use `messageId` to detect duplicates. Cancel is described as idempotent, and the cancel operation also says success is not guaranteed. This read did not show a mandatory transport idempotency key. Public tracker titles, not comment experiments: [issue 1893](https://github.com/a2aproject/A2A/issues/1893) is a closed proposal for a standard idempotency-key header, and [issue 1987](https://github.com/a2aproject/A2A/issues/1987) is an open idempotency and safe-retry epic. A reported retry count from a comment on that epic was not re-read and is not cited.

## More candidates, not prescriptions

Each item below is something to test against no change. None is a universal fix. Overlapping savings are not added. No benefit figure is claimed here.

- A floor on fetches that are actually on the path, versus extra fetches.
- A URL the tool already showed, versus another lookup by id.
- A growing conversation or tool payload, versus a static prefix.
- Queue, sandbox, or rate-limit wait, versus model delay.
- Delivery time, versus a tail of persistence or grading.
- Cache reuse, path changes, deferred tool definitions, reuse of a parsed source, independent batching, and a bounded retry of a blocked source. Each can fail its anti-fit. Measure before keeping one.

## What was left out on purpose

A RAG-paper claim that BM25 won on FEVER, a 2016-versus-2018 index swap, a prompt-cache header dated 2026-10-21, a closed community issue about `git status` in a cached prefix, a Hacker News cost anecdote, and a Reddit thread whose comments were not retrieved are omitted. They were not needed, or they were not confirmed in this pass.
