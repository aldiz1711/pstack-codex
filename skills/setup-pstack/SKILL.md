---
name: setup-pstack
description: Configure which Codex models pstack uses per role and at what reasoning budget. Detects available models and writes a PStack role map for its skills. Use for $setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

Before applying this workflow, read `poteto-mode/references/host-runtime.md`. Resolve `poteto-mode` from the catalog or explicitly as a sibling under this loaded PStack skill's verified package namespace or skill-directory parent. Do not guess a plugin ID. The reference defines resource resolution, host capabilities, and model configuration.


# Setup pstack

Write a user role map that PStack explicitly reads before model selection. On actual local Codex, preserve `${CODEX_HOME:-~/.codex}/pstack-models.md`. A trusted local `SessionStart` or `SubagentStart` hook is optional. On cloud hosts, use a verified user-selected configuration location or clearly state that the map is session-scoped. Installed skill resources are not a writable user store. Never claim persistence without a verified reload route. Model and reasoning effort remain separate values.

## Steps

### 1. Detect available models

Enumerate the model names and reasoning efforts accepted by the current Codex subagent tool or model picker. Never write a model or effort you have not confirmed is available. `inherit-parent` and `auto` mean to omit both overrides and are always valid.

### 2. Load current state

Read the supplied map or actual local map if accessible. Otherwise use `poteto-mode/references/model-config.md`, whose defaults preserve the original `unlimited (max)` budget. Keep previously chosen roles unless the current request changes them. Offer `references/profiles/sol-astra-xhigh.md` only when the user asks for that profile or a balanced Sol/Astra budget; it is not the public default.

### 3. Budget, map, and confirm

**(a) Ask for a budget when not already supplied.** Offer the four original options: `unlimited — keep max`, `large — xhigh reasoning`, `medium — high reasoning`, and `small — medium reasoning`. The default is `unlimited — keep max` when the user does not choose another budget. Name the current budget when one is recorded.

**(b) Apply it.** Store the reasoning effort separately from the model name. `unlimited` leaves each role at its listed effort. `large`, `medium`, and `small` target `xhigh`, `high`, and `medium`. If a model does not support the target effort, use its highest supported effort at or below the target or mark the role as needing a choice. Do not change `inherit-parent` or `auto`.

**(c) Show the roles and confirm.** Show every role with its model and effort, flagging unavailable choices. Offer the available models, supported efforts, `inherit-parent`, and `auto` as alternatives. Panel roles (arena runners, architect runners, interrogate reviewers) contain one entry per desired subagent, including repeated models. `arena cross-judge pool` contains choices from which Arena selects one. Independent reviews follow the [independent review policy](../poteto-mode/references/independent-review.md). They default to the parent model and effort, with model diversity optional. The current Codex concurrency limit may require running a panel in waves.

### 4. Validate

Every named model and effort must be supported by the current Codex client. `inherit-parent` and `auto` always pass. Ask the user to choose again for an unavailable value.

### 5. Write the role map

Write the chosen user configuration target idempotently, preserving unrelated state. On local Codex, retain the original home-directory route. On cloud, confirm the storage and new-task lookup route, or use a labeled session map. PStack's actual subagent calls receive separate `model` and reasoning-effort values. Missing user lines use the public bundled defaults; reviewer defaults remain `inherit-parent`. Format:

Use the role names and text format in `poteto-mode/references/model-config.md`. Copy that map as the default rather than maintaining a second default table here.

Use only confirmed available combinations. If a default is unavailable, choose an equivalent the user can access or `inherit-parent` rather than writing a broken entry.

### 6. Confirm

Read back and validate the exact map, then report the verified storage or session scope. Every PStack entrypoint loads it explicitly before delegation and after resume. A supported trusted local hook can supply the same map; cloud loading does not depend on hooks. Do not claim the parent picker or host-wide model settings changed. Re-running setup updates only the chosen user map.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with $create-verification-skill." On yes, invoke `$create-verification-skill`. On no, move on without pushing.
