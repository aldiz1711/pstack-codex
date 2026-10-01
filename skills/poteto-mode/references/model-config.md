# PStack model configuration

Resolve the role map before choosing a model. The bundled map below is the public fallback and preserves the original local defaults. A resolved bundled value counts as the role's default configuration. Missing lines in a user map fall back to this map, not to a different instruction in another skill.

Use current task instructions first, then a supplied user role map, then the actual local `${CODEX_HOME:-~/.codex}/pstack-models.md` when accessible, then these defaults. The role names and comma-separated aliases below match `$setup-pstack`. Panel entries retain one session per entry; a judge pool selects one entry. The general hardest-task default applies when no explicit role choice overrides it.

```text
# budget: unlimited (max)
feature, refactoring: gpt-6-luna | xhigh
bug-fix: gpt-6-luna | xhigh
perf-issue: gpt-6-luna | xhigh
hillclimb: gpt-6-luna | xhigh
judgment and prose: gpt-6-astra | max
hardest tasks: gpt-6-astra | max
how explorer: gpt-6-luna | xhigh
how explainer: gpt-6-astra | max
why investigators: gpt-6-luna | xhigh
why synthesizer: gpt-6-astra | max
reflect tooling: gpt-6-sol | max
reflect judgment, divergent, synthesizer: gpt-6-astra | max
arena runners: gpt-6-astra | max, gpt-6-astra | max, gpt-6-astra | max, gpt-6-astra | max
arena cross-judge pool: inherit-parent
swarm workers: gpt-6-luna | xhigh
architect runners: gpt-6-astra | max, gpt-6-astra | max, gpt-6-astra | max, gpt-6-astra | max
interrogate reviewers: inherit-parent
```

An unlisted independent reviewer or runtime verifier role inherits the parent model and effort. This is the same fallback used by the independent-review policy. `inherit-parent` and `auto` omit both launcher overrides. Separate sessions may use the same model; they do not imply model diversity.

Validate every named combination against the actual launcher. Unavailable explicit choices stay blocked until the user selects a replacement or authorizes a fallback. A model profile is optional; `$setup-pstack` offers the balanced Sol/Astra xhigh profile in `setup-pstack/references/profiles/sol-astra-xhigh.md` when requested. It does not replace these defaults automatically.
