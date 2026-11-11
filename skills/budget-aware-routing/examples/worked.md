# Example: planner and two workers (synthetic)

Task: update an API and its documentation. Planner freezes the response contract. Code writer owns implementation; docs writer uses that contract; reviewer checks the actual behavior after integration.

The first planner request has a nominal $0.10 budget but includes a large tool/system payload. If the host checks cost only after the response, it may exceed the nominal budget before refusing another call.

Safe plan: inspect limit semantics and request size before a paid probe; do not promise a hard cap without enforcement evidence. An offline JSON handoff that parses successfully proves the format, not live routing, quota isolation, or completion.
