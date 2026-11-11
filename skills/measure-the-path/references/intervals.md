# Interval input

Supply JSON with finite numeric `window_start`, `window_end`, and a nonempty `spans` array. Each span has a nonempty `name`, finite `start`, and finite `end`. Times use a common clock and unit, with start no later than end, within the observation window.

Output: `wall_time`, `summed_work`, `covered_time`, `unexplained_time`, and `gaps`. Nested and overlapping intervals are merged for coverage. A zero-duration event covers no time.

This does not infer causality, dependencies, exclusive CPU time, or a critical path. Gaps can reflect instrumentation omissions rather than inactivity. Use separate data for token usage and costs.
