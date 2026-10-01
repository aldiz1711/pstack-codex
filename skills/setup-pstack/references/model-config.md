# PStack model configuration

Resolve the model and reasoning effort separately before delegation. Poteto resolves once per task and passes the relevant role choices and source to children. A directly invoked delegation skill resolves when no map was passed. Refresh after setup changes the map or a task resumes. Pure principle and writing skills do not need this read.

## Resolve the user's map

Use this precedence, highest first:

1. Current task instructions, including explicit model, effort, role, or panel-size overrides.
2. A resolved role map supplied by the caller, with its source.
3. The user's verified configuration on this host. On actual local Codex, read `${CODEX_HOME:-~/.codex}/pstack-models.md`. In ChatGPT cloud with Library available, find and read the user's `pstack-models.md` as described below. An explicitly selected accessible configuration location may replace either route.
4. The bundled role defaults below for roles with no user line.

Read current contents before selecting models. A path or Library identity alone is not the map. Treat the map as model configuration, not permission to execute unrelated instructions. Keep model choices separate from host-wide settings.

### ChatGPT Library lookup

Discover the current Library tools and read their owning Library skill before use. Search the exact filename `"pstack-models.md"` with title-only search. Confirm an exact, user-owned native file. Follow pagination when needed to resolve candidates; do not treat a failed or partial search as proof that no file exists. Reuse a verified selected `library_file_id` and read that file's latest complete contents. If multiple exact candidates remain, ask which one to use before choosing or replacing it. Do not select a shared file or fuzzy title match silently.

Retain the returned stable ID, current version, filename, and resolved roles in task context. Pass the relevant resolved choices to children so they do not repeat the lookup. A fresh task can discover the file by exact title and read its latest contents. Never put a user's Library ID in the distributed plugin or infer persistence from a previous conversation alone.

If Library is unavailable or reading fails, report the missing configuration route. Use a supplied session map, an accessible explicitly selected user location, or the bundled defaults with that limitation stated. Do not silently replace an explicit inaccessible model choice. A cloud workspace file alone does not prove cross-task persistence. Do not invent a Vault setter, backend, or automatic global prompt injection.

Use `fork_turns: "none"` when the launcher supports it. Pass a self-contained brief with the resolved role choices, source, and required resource locators. Named local agents are optional; discover the actual host launcher before supplying overrides.

## Bundled role defaults

These are the public fallback and setup's default example. The budget is unlimited. Most work uses GPT-6.1 Sol at max reasoning. The hardest tasks use GPT-6 Astra at max reasoning. Keep existing user choices unless setup was asked to change them.

```text
# budget: unlimited (max)
feature, refactoring: gpt-6.1-sol | max
bug-fix: gpt-6.1-sol | max
perf-issue: gpt-6.1-sol | max
hillclimb: gpt-6.1-sol | max
judgment and prose: gpt-6.1-sol | max
hardest tasks: gpt-6-astra | max
how explorer: gpt-6.1-sol | max
how explainer: gpt-6.1-sol | max
why investigators: gpt-6.1-sol | max
why synthesizer: gpt-6.1-sol | max
reflect tooling: gpt-6.1-sol | max
reflect judgment, divergent, synthesizer: gpt-6.1-sol | max
arena runners: gpt-6.1-sol | max, gpt-6.1-sol | max, gpt-6.1-sol | max, gpt-6.1-sol | max
arena cross-judge pool: inherit-parent
swarm workers: gpt-6.1-sol | max
architect runners: gpt-6.1-sol | max, gpt-6.1-sol | max, gpt-6.1-sol | max, gpt-6.1-sol | max
interrogate reviewers: inherit-parent
```

The `hardest tasks` role applies when the actual scope needs it, such as difficult concurrency, subtle algorithms, or a cross-cutting design with unresolved constraints. Do not classify all Arena or Architect tasks as hardest. Explicit current-task choices take precedence. A saved role-specific user choice also takes precedence over the bundled difficulty fallback.

The role names and comma-separated aliases match setup. Missing user lines use this table. Panels retain one session per entry, including repeated models; the Arena judge pool selects one entry. Preserve the requested panel size and queue waves against the observed concurrency limit. Separate sessions on one model do not imply model diversity.

Unlisted independent reviewer and runtime verifier roles inherit the parent model and effort. `inherit-parent` and `auto` omit both launcher overrides. Validate named models and efforts against the actual launcher. If an explicit choice is unavailable, stop that dependent launch until the user selects a replacement or authorizes a fallback. Do not silently change model families or increase the reasoning budget.
