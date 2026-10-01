# PStack for Codex

An unofficial Codex adaptation of [PStack](https://github.com/cursor/plugins/tree/main/pstack), the engineering skills and playbooks created by [Lauren Tan (Poteto)](https://github.com/poteto). This repository keeps PStack's workflows and principles while mapping Cursor-specific integration to Codex.

PStack's central idea is simple: make fewer changes, verify them against real behavior, and use parallel agents only when their work can be reviewed. [`$poteto-mode`](./skills/poteto-mode/SKILL.md) chooses a playbook for the task and calls the other skills as needed.

This is a community adaptation, not an official PStack release from Poteto or Cursor.

## Install

Add this repository as a Codex plugin marketplace, then install the plugin:

```sh
codex plugin marketplace add aldiz1711/pstack-codex
codex plugin add pstack-codex@pstack-codex
```

Start a new Codex task so it loads the installed skills. On ChatGPT cloud, invoke the skills through their installed packages. A missing named local role uses the same packaged prompt through a supported delegate. Required read-only review still needs an enforced boundary; a prompt alone does not satisfy it. Review the bundled hook if Codex asks, then trust it if you want PStack to load your model configuration at task and subagent startup. The hook reads `~/.codex/pstack-models.md` when that file exists; PStack also has working defaults without it.

Use PStack directly with its inline defaults. `$setup-pstack` is optional and changes your reasoning budget or models per role. Its default budget remains **unlimited (max)**. Use `$poteto-mode` on a real task:

```text
$poteto-mode reproduce this bug, fix its root cause, and verify the result in the running app.
```

See the [setup guide](./docs/guide/01-setup.md) for model configuration and pull request review setup. The [full guide](./docs/guide/README.md) covers the workflows from investigation through verification and shipping.

## Package this source for ChatGPT

This PR is a source candidate. Check out its branch or exact commit before evaluating it. Packaging does not install the candidate or publish a release.

```sh
python3 scripts/package-plugin.py
python3 -m unittest discover -s tests
python3 scripts/package-plugin.py --output ../pstack-codex-account.zip
```

Packaging requires Git and Python 3.9 or newer. The account archive contains all 49 skills, 23 playbooks, resources, helpers, roles, hooks, assets, and licenses. It exports tracked source files, excludes private untracked or ignored files, and omits only the local marketplace registration `.agents/plugins/marketplace.json`. Add intended new source files to the Git index before packaging. Use `--source` to retain the marketplace registration for local/source distribution. Use the supported private Plugin Creator archive-import route for an account install.

Local model maps and trusted hooks keep their original behavior. Cloud tasks can use the inline defaults without setup, Library, or a local home-directory map. If you explicitly configure cloud roles, setup reports their verified storage or current-task scope. The plugin does not create a cloud startup hook.

Bun helpers require Bun, their locked dependencies, and the original forge access on a real executor. Orchestrate keeps its original Graphite requirement. Missing capabilities do not authorize weaker proof or a different workflow. The candidate validation workflow checks the complete package and original Bun tests/typecheck.

## What PStack does

- **Routes work through playbooks.** `$poteto-mode` covers investigation, bug fixes, features, refactoring, performance, PR babysitting, shipping, and longer autonomous runs. It stays active in the task until you opt out.
- **Uses focused skills and principles.** `$how`, `$why`, `$architect`, `$arena`, `$swarm`, `$interrogate`, and the verification skills can also be called directly. The [guide](./docs/guide/README.md) and [`poteto-mode` skill](./skills/poteto-mode/SKILL.md) lead to the full instructions.
- **Makes review and proof explicit.** Agents inspect diffs, check claims against the code, and exercise the real app where the playbook requires it. `$interrogate` runs PStack's local review panel.
- **Lets you configure model roles.** `$setup-pstack` writes `~/.codex/pstack-models.md`. The current defaults use GPT-6 Luna for scoped code work and GPT-6 Astra for the hardest judgment and design tasks. Independent reviewers default to the parent model and reasoning effort. Explicit reviewer choices take precedence.

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
| Model choices loaded into agent sessions | `$setup-pstack` writes a role map; the bundled Codex hook loads it at task and subagent startup. |
| Durable objectives and recurring audits | Codex `/goal` and scheduled follow-ups. |
| Parallel workers and independent reviewers | Codex subagents and isolated worktrees; read-only roles use a registered `pstack-readonly` agent or an equivalent supported delegate with an enforced read-only boundary. |
| Local code review | `$interrogate` keeps PStack's review workflow; Codex `/review` is also available. |
| Automated GitHub PR review | Enable [Codex Cloud Code Review](https://developers.openai.com/codex/cloud/code-review) separately for the repository. PStack's babysit playbook then triages its review threads. |

Cursor supports a wider mix of model providers. To keep Arena candidates at comparable capability in Codex, the default Arena runs four independent GPT-6 Astra candidates at max reasoning. Its separate, read-only judge uses the configured choice or the parent model and effort. `$setup-pstack` can change this panel. Model diversity is optional. Independent runs of one model can still share blind spots, so reviewers must support their findings with evidence.

## Credits and licenses

[Original PStack](https://github.com/cursor/plugins/tree/main/pstack) was created by Lauren Tan and is included under its [MIT license](./licenses/pstack-LICENSE). The bundled `$control-cli`, `$control-ui`, and `$deslop` skills come from [Cursor Team Kit](https://github.com/cursor/plugins/tree/main/cursor-team-kit/skills) under its [MIT license](./licenses/cursor-team-kit-LICENSE). The Codex adaptation is covered by this repository's [MIT license](./LICENSE).
