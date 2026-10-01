# Set up pstack

In this page you install the plugin, pick which models pstack uses, and run your first task. Local installation stays the same. A cloud host resolves skill resources and model configuration explicitly.

## Install the plugin

The commands below install this repository's default branch. To evaluate a draft candidate, check out its branch or exact commit. Build a standalone ChatGPT account archive with `python3 scripts/package-plugin.py --output ../pstack-codex-account.zip`, then use the supported private Plugin Creator import route. The source retains local marketplace registration; the standalone account ZIP deliberately omits it. See the [packaging instructions](../../README.md#package-this-source-for-chatgpt). A draft source version is not a published release.

Add this repository as a Codex plugin marketplace and install PStack:

```sh
codex plugin marketplace add aldiz1711/pstack-codex
codex plugin add pstack-codex@pstack-codex
```

Codex confirms the plugin is installed. Start a new task to load its skills.

## Set up pull request reviews

PStack's local independent review is `$interrogate`. Codex also provides `/review` for local changes. If the `review-agent` skill is available, you can delegate a local review to an ordinary Codex subagent and instruct it to read that skill; `review-agent` is the skill it follows, not a named subagent type. For Cursor Bugbot's GitHub role, connect the repository to Codex Cloud and enable Code Review in Codex settings. Ask for a review with `@codex review`, or enable automatic reviews for the repository. Put repository-specific reviewer guidance under `## Code Review Rules` in the applicable `AGENTS.md`. PStack's Babysit playbook triages the resulting PR threads; installing PStack does not enable Codex Cloud reviews for a repository. GitHub Codex Code Review currently publishes P0/P1 findings, so it may not report every class of finding Bugbot reports. Keep `$interrogate` for PStack's local review. See [Codex Code Review](https://developers.openai.com/codex/cloud/code-review) and the [local `/review` guide](https://learn.chatgpt.com/docs/code-review).

## Pick your models

Run:

```text
$setup-pstack
```

[`$setup-pstack`](../../skills/setup-pstack/SKILL.md) detects the models and reasoning efforts you have access to, asks for a budget, shows you each role (code delegates, judgment, the review panels), and asks what you want. The default budget is unlimited. Answer the questions. It preserves `~/.codex/pstack-models.md` on actual local Codex. On ChatGPT cloud it can create or update your `pstack-models.md` in Library, then read its latest contents before model selection. It reuses the file identity and asks you to resolve duplicate filenames. If Library is unavailable, it reports session scope or uses your selected accessible configuration location. Poteto resolves once and passes choices to children; directly invoked delegation skills load the map when needed. Trusted local hooks remain optional.

The [bundled role map](../../skills/setup-pstack/references/model-config.md) uses GPT-6.1 Sol max for ordinary roles and GPT-6 Astra max for the hardest tasks. Arena and Architect retain four-session panels. Independent reviewers and the Arena judge inherit the parent. Setup offers the example inline, without a separate preference profile.

You only override what you care about. A role with no line in the rule keeps the skill's default. To restore a default later, delete that role's line, or just run `$setup-pstack` again.

You might be wondering what happens if you use Auto. Set a role to `inherit-parent` or `auto` and pstack omits both subagent model and reasoning-effort overrides, so the subagent inherits your parent chat model. Both values mean the same thing, and neither is a model slug. For a panel role the value is a list, and one subagent runs per entry, so the list length sets the panel size. Setup also configures `swarm workers`, the default model for every `$swarm` worker unless a race names a model for each arm.

## Accept the verification offer, or don't

At the end of setup, `$setup-pstack` looks for a way to prove app behavior in your project, either a `verify-*` skill or an existing harness. If it finds neither, it offers once to generate one with [`$create-verification-skill`](../../skills/create-verification-skill/SKILL.md).

Say yes and it writes `.agents/skills/verify-<app>/`, a project-local skill that teaches agents to drive your app the way a user does. It proves the skill works once before handing it over. Say no and setup moves on. You can run `$skill-creator` yourself any time. [Verify and ship](./06-verify-and-ship.md#create-a-project-verification-skill) covers when it earns its place.

A compatible local hook may supply the same map after review/trust. Cloud operation does not depend on it. Readback and a supported new-task lookup route are required before relying on persistent configuration.

## Run your first task

Pick something real but small, and describe it the way you'd describe it to a colleague:

```text
$poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

Watch the todo list. Its first items are the matched playbook's steps copied in, the Feature playbook for this prompt. If `$poteto-mode` skips a step, the step stays in the list with `skip: <reason>`, so you can see what it chose not to do.

From here you can type normal follow-ups. `$poteto-mode` is sticky. It stays on for the conversation until you opt out by saying so.

Next: [Route work through `$poteto-mode`](./02-poteto-mode.md).
