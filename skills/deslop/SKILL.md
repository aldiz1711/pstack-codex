---
name: deslop
description: Remove AI-generated code slop and clean up code style
---

Before applying this workflow, read `poteto-mode/references/host-runtime.md`. Resolve `poteto-mode` from the catalog or explicitly as a sibling under this loaded PStack skill's verified package namespace or skill-directory parent. Do not guess a plugin ID. The reference defines resource resolution, host capabilities, and model configuration.


# Remove AI code slop

Check the diff against main and remove AI-generated slop introduced in the branch.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Keep the final summary concise (1-3 sentences).
