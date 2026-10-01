# PStack for Codex

An unofficial Codex adaptation of [PStack](https://github.com/cursor/plugins/tree/main/pstack), the engineering skills and playbooks created by [Lauren Tan (Poteto)](https://github.com/poteto). This repository keeps PStack's workflows and principles while mapping integration to the actual local or cloud host. The original local model defaults and invocation policies remain unchanged.

PStack's central idea is simple: make fewer changes, verify them against real behavior, and use parallel agents only when their work can be reviewed. [`$poteto-mode`](./skills/poteto-mode/SKILL.md) chooses a playbook for the task and calls the other skills as needed.

This is a community adaptation, not an official PStack release from Poteto or Cursor.

## Install

These repository commands install the default branch. A draft PR is source under review, not a published release. To evaluate a candidate, check out its branch or exact commit first and use the source-based packaging instructions below.

Add this repository as a Codex plugin marketplace, then install the plugin:

```sh
codex plugin marketplace add aldiz1711/pstack-codex
codex plugin add pstack-codex@pstack-codex
```

Start a new task so it discovers the installed skills. Manual-only skills, including Poteto Mode, stay explicit-only. The shared [host runtime](./skills/poteto-mode/references/host-runtime.md) resolves their owning resources even when an automatic catalog omits them. A trusted local hook can supply `~/.codex/pstack-models.md`; every workflow also loads configuration explicitly, so cloud operation does not depend on hooks.

Run `$setup-pstack` to choose a reasoning budget and models for each role. Its default budget is **unlimited (max)**. Then use `$poteto-mode` on a real task:

```text
$poteto-mode reproduce this bug, fix its root cause, and verify the result in the running app.
```

See the [setup guide](./docs/guide/01-setup.md) for model configuration and pull request review setup. The [full guide](./docs/guide/README.md) covers the workflows from investigation through verification and shipping.

## Package this source for ChatGPT

Run from a checkout of the exact branch or commit you intend to install. Python 3.9 or newer is sufficient for the packager.

```sh
python3 scripts/package-plugin.py
python3 -m unittest discover -s tests
python3 scripts/package-plugin.py --output ../pstack-codex-account.zip
```

The account ZIP contains one `pstack-codex` directory and all 49 skills, 23 playbooks, resources, scripts, and licenses. It excludes only the local marketplace registration `.agents/plugins/marketplace.json`, plus Git metadata, dependency caches, and build output. The original registration remains in source. Use the supported Plugin Creator archive-import route for a private account install; packaging alone does not install or publish it. No public release asset or OpenAI directory submission is created by these commands.

For a source archive that retains marketplace registration, add `--source`. That archive is for source/local distribution and is not the standalone account-import ZIP. Both forms use stable file order, normalized permissions, and fixed timestamps; the command reports their SHA-256.

The proposed `0.15.3-dev.1` source version orders above `0.15.2` under SemVer. It is not a published tag, and automatic host upgrade behavior has not been verified.

## What PStack does

- **Routes work through playbooks.** `$poteto-mode` covers investigation, bug fixes, features, refactoring, performance, PR babysitting, shipping, and longer autonomous runs. It stays active in the task until you opt out.
- **Uses focused skills and principles.** `$how`, `$why`, `$architect`, `$arena`, `$swarm`, `$interrogate`, and the verification skills can also be called directly. The [guide](./docs/guide/README.md) and [`poteto-mode` skill](./skills/poteto-mode/SKILL.md) lead to the full instructions.
- **Makes review and proof explicit.** Agents inspect diffs, check claims against the code, and exercise the real app where the playbook requires it. `$interrogate` runs PStack's local review panel.
- **Lets you configure model roles.** `$setup-pstack` preserves the local configuration route or uses a verified cloud user store/session map. The [public defaults](./skills/poteto-mode/references/model-config.md) retain GPT-6 Luna xhigh for scoped code work, Astra max for judgment/hardest tasks, and parent-inheriting independent reviewers. The [Sol/Astra xhigh profile](./skills/setup-pstack/references/profiles/sol-astra-xhigh.md) is optional. Actual launcher availability is checked before delegation.

For example:

```text
$how does cancellation flow through this service?
$arena compare several designs for this API boundary.
$interrogate review the current diff.
```

## How this maps to Codex

PStack's playbooks, skill instructions, and engineering principles remain the source of the workflow. The integration points use Codex mechanisms:

| PStack need | Codex mechanism |
| --- | --- |
| Model choices loaded into agent sessions | Every entrypoint explicitly resolves the role map. A supported trusted local Codex hook is optional. |
| Durable objectives and recurring audits | Supported host objectives and wakeups. Missing equivalents remain blocked. |
| Parallel workers and independent reviewers | Supported subagents and isolated outputs. An enforced read-only gate requires verified permissions; a role name or worktree alone is insufficient. |
| Local code review | `$interrogate` keeps PStack's review workflow; Codex `/review` is also available. |
| Automated GitHub PR review | Enable [Codex Cloud Code Review](https://developers.openai.com/codex/cloud/code-review) separately for the repository. PStack's babysit playbook then triages its review threads. |

Cursor supports a wider mix of model providers. To keep Arena candidates at comparable capability in Codex, the default Arena runs four independent GPT-6 Astra candidates at max reasoning. Its separate, read-only judge uses the configured choice or the parent model and effort. `$setup-pstack` can change this panel. Model diversity is optional. Independent runs of one model can still share blind spots, so reviewers must support their findings with evidence.

## Verification and supported boundaries

The package requires no MCP server. Shell, forge, browser, local-app, and durable-task capabilities still come from the host. Original Bun helpers require Bun and their locked dependencies on a real writable executor. Orchestrate retains its original Graphite `gt` frontier requirement. Optional command hooks are supported only in a compatible local POSIX/Python environment after trust; cloud explicit loading is the fallback. Native Windows hook execution is not claimed.

The read-only PR workflow runs these package checks plus the original Bun helper suite and typecheck. It does not publish an archive or grant write permissions. Run helper tests locally where Bun is available:

```sh
cd skills/poteto-mode/scripts
bun install --frozen-lockfile
bun run test
bun run typecheck
```

Metadata and archive checks do not prove runtime verification. A host without enforced read-only permissions can return labeled advisory review but cannot satisfy that gate. Missing or partial task history cannot prove a worktree is unused. The local audit retains its platform/path assumptions; verify its inputs before pruning.

## Credits and licenses

[Original PStack](https://github.com/cursor/plugins/tree/main/pstack) was created by Lauren Tan and is included under its [MIT license](./licenses/pstack-LICENSE). The bundled `$control-cli`, `$control-ui`, and `$deslop` skills come from [Cursor Team Kit](https://github.com/cursor/plugins/tree/main/cursor-team-kit/skills) under its [MIT license](./licenses/cursor-team-kit-LICENSE). The Codex adaptation is covered by this repository's [MIT license](./LICENSE).
