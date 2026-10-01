# Optional balanced Sol/Astra profile

Use this profile only when the user chooses it. Copy its role map to the selected user configuration location; do not edit installed resources. Resolve `poteto-mode/references/host-runtime.md` through PStack before selecting a model. Validate availability in the actual launcher.

Ordinary engineering, prose, exploration, synthesis, and review use `gpt-6.1-sol` at `xhigh`. The hardest tasks use `gpt-6-astra` at `xhigh`, including cross-cutting design, subtle algorithms, and difficult concurrency. Apply that difficulty tier over a generic profile role default; a user's explicit model or configured role takes precedence. Do not raise the effort to `max` without instruction.

```text
# budget: large (xhigh)
feature, refactoring: gpt-6.1-sol | xhigh
bug-fix: gpt-6.1-sol | xhigh
perf-issue: gpt-6.1-sol | xhigh
hillclimb: gpt-6.1-sol | xhigh
judgment and prose: gpt-6.1-sol | xhigh
hardest tasks: gpt-6-astra | xhigh
how explorer: gpt-6.1-sol | xhigh
how explainer: gpt-6.1-sol | xhigh
why investigators: gpt-6.1-sol | xhigh
why synthesizer: gpt-6.1-sol | xhigh
reflect tooling: gpt-6.1-sol | xhigh
reflect judgment, divergent, synthesizer: gpt-6.1-sol | xhigh
arena runners: gpt-6.1-sol | xhigh, gpt-6.1-sol | xhigh, gpt-6.1-sol | xhigh, gpt-6.1-sol | xhigh
arena cross-judge pool: gpt-6.1-sol | xhigh
swarm workers: gpt-6.1-sol | xhigh
architect runners: gpt-6.1-sol | xhigh, gpt-6.1-sol | xhigh, gpt-6.1-sol | xhigh, gpt-6.1-sol | xhigh
interrogate reviewers: gpt-6.1-sol | xhigh
```

Panel entries each create one separate session, including repeated models. Four Sol sessions are four reviewers or runners, not four model families. A strongest-model task may use Astra for the required sessions while preserving their isolation and evidence rules.
