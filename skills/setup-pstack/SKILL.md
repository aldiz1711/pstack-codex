---
name: setup-pstack
description: Configure which Codex models pstack uses per role and at what reasoning budget. Detects available models and writes a PStack role map for its skills. Use for $setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Setup is optional. The inline defaults work without a saved role map. On local Codex, write `~/.codex/pstack-models.md`, the role map that pstack skills read before choosing a Codex subagent model and reasoning effort. The bundled `SessionStart` and `SubagentStart` hooks also load it into new Codex tasks and subagents. If `CODEX_HOME` is set, use that directory instead of `~/.codex` throughout this skill. On a cloud host without the local home-directory route, keep the chosen map in the current task or use an accessible user-selected configuration location. Verify any claimed storage and reload route. Local hooks are not a cloud startup mechanism. Codex has no Cursor `.mdc` rule or model slug with effort encoded at the end.

## Steps

### 1. Detect available models

Enumerate the model names and reasoning efforts accepted by the current Codex subagent tool or model picker. Never write a model or effort you have not confirmed is available. `inherit-parent` and `auto` mean to omit both overrides and are always valid.

### 2. Load current state

On local Codex, if `~/.codex/pstack-models.md` exists, read its budget and role values. On cloud, read the current task map or the explicitly selected accessible user map when one exists. Otherwise start from the `unlimited (max)` budget and role defaults in step 5. Keep any role that the user previously changed when rerunning setup.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Offer the four original options: `unlimited — keep max`, `large — xhigh reasoning`, `medium — high reasoning`, and `small — medium reasoning`. The default is `unlimited — keep max` when the user does not choose another budget. Name the current budget when one is recorded.

**(b) Apply it.** Store the reasoning effort separately from the model name. `unlimited` leaves each role at its listed effort. `large`, `medium`, and `small` target `xhigh`, `high`, and `medium`. If a model does not support the target effort, use its highest supported effort at or below the target or mark the role as needing a choice. Do not change `inherit-parent` or `auto`.

**(c) Show the roles and confirm.** Show every role with its model and effort, flagging unavailable choices. Offer the available models, supported efforts, `inherit-parent`, and `auto` as alternatives. Panel roles (arena runners, architect runners, interrogate reviewers) contain one entry per desired subagent, including repeated models. `arena cross-judge pool` contains choices from which Arena selects one. Independent reviews follow the [independent review policy](../poteto-mode/references/independent-review.md). They default to the parent model and effort, with model diversity optional. The current Codex concurrency limit may require running a panel in waves.

### 4. Validate

Every named model and effort must be supported by the current Codex client. `inherit-parent` and `auto` always pass. Ask the user to choose again for an unavailable value.

### 5. Write the role map

On local Codex, overwrite `~/.codex/pstack-models.md` so reruns stay idempotent. On cloud, update the confirmed user-selected target or return a clearly labeled task-scoped map; do not write into installed plugin resources. This is PStack's role map, loaded by the bundled hooks and read by its skills; Codex's actual subagent calls receive separate `model` and reasoning-effort values. A role with no line keeps its skill default. Format:

```text
# pstack model configuration. Delete a line to use the skill default.
# budget: unlimited (max)
feature, refactoring: gpt-6.1-sol | xhigh
bug-fix: gpt-6.1-sol | xhigh
perf-issue: gpt-6.1-sol | xhigh
hillclimb: gpt-6.1-sol | xhigh
judgment and prose: gpt-6.1-sol | max
hardest tasks: gpt-6-astra | max
how explorer: gpt-6.1-sol | xhigh
how explainer: gpt-6.1-sol | max
why investigators: gpt-6.1-sol | xhigh
why synthesizer: gpt-6.1-sol | max
reflect tooling: gpt-6.1-sol | max
reflect judgment, divergent, synthesizer: gpt-6.1-sol | max
arena runners: gpt-6.1-sol | max, gpt-6.1-sol | max, gpt-6.1-sol | max, gpt-6.1-sol | max
arena cross-judge pool: inherit-parent
swarm workers: gpt-6.1-sol | xhigh
architect runners: gpt-6-astra | max, gpt-6-astra | max, gpt-6-astra | max, gpt-6-astra | max
interrogate reviewers: inherit-parent
```

Use only confirmed available combinations. If a default is unavailable, choose an equivalent the user can access or `inherit-parent` rather than writing a broken entry.

### 6. Confirm

Report the verified target or task scope. Read back saved choices before claiming that they were written. On local Codex, the bundled hook loads it when a Codex task starts, resumes, or compacts, and when a subagent starts. On cloud, pass the selected role choices explicitly to delegates; do not claim automatic cross-task loading without a verified host route. Codex requires the user to review and trust a new or changed plugin hook before it runs; direct them to Codex's hook review (`/hooks` in the CLI) if this hook is pending. Do not claim automatic loading until the hook is trusted. Re-running this skill updates the model map without changing the hook definition.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with $create-verification-skill." On yes, invoke `$create-verification-skill`. On no, move on without pushing.
