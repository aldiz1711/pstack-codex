---
name: setup-pstack
description: Configure which models PStack uses per role and at what reasoning budget. Detect available models and save a user role map on local Codex or in ChatGPT Library. Use for $setup-pstack, "configure pstack models", "pstack budget", or changing PStack's model choices.
---

# Setup pstack

Read `references/model-config.md` for the shared loading contract and bundled role map. Read `poteto-mode/references/host-runtime.md` through the verified PStack namespace or skill-directory parent for host capabilities. Preserve the user's existing choices unless this request changes them.

## 1. Detect available models

Enumerate model names and reasoning efforts accepted by the actual subagent launcher or model picker. Confirm each named combination before saving it. `inherit-parent` and `auto` omit both overrides and are always valid.

## 2. Load current state

Read the chosen saved target's latest complete contents as the edit base before applying requested changes. Launch-resolution precedence does not choose the persistence base. Do not save task-only overrides or caller-resolved defaults unless the user asks to persist them. If no saved map exists, use the bundled map or a user-supplied map as the initial base. On actual local Codex, keep `${CODEX_HOME:-~/.codex}/pstack-models.md`. On ChatGPT cloud, use the user's exact `pstack-models.md` in Library when its tools are available. Resolve duplicate candidates before writing. An installed plugin reference is the public default, not a user store.

## 3. Choose the budget and roles

Ask for a budget only when the user has not supplied one. Offer `unlimited` for max reasoning, `large` for xhigh, `medium` for high, and `small` for medium. The default is unlimited. Show the recorded budget when there is one.

The default example uses GPT-6.1 Sol max for ordinary work, including four-session Arena and Architect panels. GPT-6 Astra max handles the hardest tasks when the actual scope warrants it. Independent reviewers and the Arena judge inherit the parent. For example, these ordinary and hardest-task entries show the format. The complete canonical role map remains in `references/model-config.md`.

```text
# budget: unlimited (max)
feature, refactoring: gpt-6.1-sol | max
hardest tasks: gpt-6-astra | max
```

Keep the model and reasoning effort separate. Unlimited preserves each selected role's listed effort. Other budgets target their named effort. If a model does not support it, show its highest supported effort at or below the target and ask for a choice. Preserve `inherit-parent` and `auto`.

Show all roles, available alternatives, unavailable combinations, and panel sizes. Repeated panel entries create separate sessions. A judge pool selects one entry. Respect the observed concurrency limit by running waves. Confirm the requested role map and its storage destination before saving when the request has not already specified them.

## 4. Validate

Check every named model and effort against this host's launcher. An unavailable explicit choice needs a user-selected replacement or authorized fallback. Do not silently substitute a model or effort. Apply only the requested or confirmed changes to the saved base. Current-task overrides still govern launches without becoming stored choices automatically.

## 5. Save the user map

Use the text format in `references/model-config.md`. Update idempotently and preserve unrelated content.

- On local Codex, write the existing home-directory map. Keep trusted `SessionStart` and `SubagentStart` hooks available; setup does not silently enable trust or alter host model settings.
- On ChatGPT cloud with Library available, read the current Library skill and discover its supported write tools. For an existing user-owned map, replace the same confirmed `library_file_id` and pass its observed version guard when supported. Create `pstack-models.md` only after a successful lookup establishes that there is no existing identity. Retain the returned ID, filename, and version. Follow the Library skill's upload and local identity requirements. On a version conflict, read the latest map and reconcile the requested change without dropping concurrent edits.
- If Library is unavailable, use an accessible user-selected configuration location or a labeled session map. Explain that a fresh task must be given that map unless its storage and lookup route have been verified. Do not claim a cloud workspace file, saved environment, or Vault value is writable or globally persistent without support.

Do not modify bundled plugin defaults as a way to save one user's choices. Never add private Library IDs or workspace paths to the distributed plugin.

## 6. Verify and report scope

Read the saved map's latest complete contents and compare them with the confirmed choices. For Library, retain the stable identity and verify that exact-title lookup resolves the intended file; a fresh task can then use the model contract's lookup path. If lookup is delayed or ambiguous, report that limitation rather than creating another file.

Report the verified storage, budget, and changed roles. Pass the refreshed resolved choices and source to the current task. Model-selecting entrypoints load explicitly; pure principle and writing leaves need no repeated loading. Trusted local hooks remain optional. Saving the map does not change the parent picker or create an always-on cloud startup hook.

## 7. Offer a verification skill when useful

Check for a project-local `verify-*` skill or existing real-app harness. If neither exists, offer once to generate one with `$create-verification-skill`. Proceed only if the user wants it.
