# Glossary

1. **Agent** — a program that selects actions to pursue a task.
2. **Tool** — a callable capability exposed to an agent.
3. **Executor** — component that runs or rejects requested tool actions.
4. **Proposal** — recorded request for an action; not proof it ran.
5. **Execution** — a tool invocation with an observed result.
6. **Approval** — an explicit authorization decision for a specific action.
7. **Denial** — explicit rejection of an action by policy or user.
8. **Prompt injection** — untrusted content attempting to alter an agent's instructions.
9. **Indirect injection** — injection delivered through retrieved content rather than the user prompt.
10. **Attack surface** — interfaces through which an adversary may influence behavior.
11. **Threat model** — structured account of assets, actors, boundaries, threats, and controls.
12. **Synthetic fixture** — fabricated test data that cannot access a real external system.
13. **Side effect** — state change caused by a tool, such as creating a draft.
14. **Read-only tool** — tool intended to observe rather than change state.
15. **Least privilege** — granting only capabilities needed for the task.
16. **Authorization** — policy decision that an action is permitted.
17. **Confirmation integrity** — ensuring approval still matches the exact action being executed.
18. **Trace** — ordered record of events in a test run.
19. **Evidence** — observed data supporting a conclusion.
20. **Attack success** — an evidenced prohibited effect, not mere exposure or attempted action.
21. **False refusal** — refusal of a legitimate task that policy permits.
22. **Negative control** — test expected not to trigger the target failure.
23. **Regression** — previously correct behavior that breaks after a change.
24. **Reproducibility** — ability to repeat a run and obtain the same results under stated conditions.
25. **Inconclusive** — evidence insufficient to label the result as success or failure.
