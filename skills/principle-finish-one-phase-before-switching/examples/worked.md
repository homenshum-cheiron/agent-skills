# Example: finish one phase before switching (synthetic)

Made up for illustration. No real person, team or run.

An agent proposes opening a branch for a new export format while the import parser (phase P1) is half done. `focus_check.py gate-open P2` fails: P1 is still open. The export idea goes into the queue with a next step for tomorrow, and P1 keeps its 16:00 end time.
