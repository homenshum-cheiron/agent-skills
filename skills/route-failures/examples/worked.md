# Example: no new records (synthetic)

Input: a source was expected to be checked today; search returns no new records.

Do not conclude “the source published nothing.” Ask for the run identity and boundaries:

- No scheduled attempt exists: scheduling/coverage incident.
- Attempt exists, HTTP timeout before discovery: network incident.
- HTTP succeeds but a changed page yields no known selectors: parser/site-change incident.
- Discovery succeeds but ingestion fails: ingestion incident.
- Ingestion and retrieval succeed, agent omits the result: reasoning/evaluation incident.

Admin output: “Attempt demo-12, discovery timed out; no completeness claim; retry owner assigned under the source policy.” Product output must stay within the evidence actually retrieved and the product's answer contract, without leaking internal health counters.
