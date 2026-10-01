# PStack host runtime

Load this reference when entering Poteto or directly invoking a delegation workflow without a supplied runtime context. Pass its discovered locator to delegates. Model loading is defined by `setup-pstack/references/model-config.md`. These references adapt the host boundary; the original skill and matched playbook own the engineering workflow. Do not load every skill or playbook.

## Resolve resources

- Prefer the owning skill's entry in the current catalog and use its returned package/main resource. For duplicates, select the same verified PStack plugin namespace as the caller; otherwise report the ambiguity. Do not guess a plugin ID or installation path.
- Manual-only skills may be omitted from the automatic catalog while still supporting explicit reads. Read `references/skill-index.json` for the canonical sibling names. On a host whose loaded PStack package is `skill://<verified-namespace>/<skill-name>`, retain that verified namespace and replace only the indexed final skill segment. Explicitly read the resulting owning package and its `SKILL.md`, then use the returned resource root for contained references. This uses a known namespace and packaged name, not a guessed plugin ID. On filesystem hosts, use the verified skills-directory parent. If explicit resolution is unsupported or denied, report the exact missing resource and stop that dependent route; do not change invocation flags or bypass a denial.
- With filesystem access, resolve from the actual loaded skill directory. Never resolve a bundled path from the repository's current working directory. `references/`, `scripts/`, and `playbooks/` paths name resources under the owning skill root. Markdown links beginning with `../` resolve from the document directory; if they cross a skill root, discover that other skill and use its package.
- A bare skill name or `$skill-name` is a request to discover and read that skill, not a shell command. `<plugin-root>/skills/<name>/...` in legacy examples means the discovered owning skill resource, or an actual verified local installation root. It is not a literal cloud path.
- Named agents are optional host registrations. Without one, use an ordinary supported subagent and give it the task-specific prompt plus discovered resource locators. Poteto's fallback is `poteto-mode/references/poteto-agent.md`; Comment Sicko's is `no-comments/references/comment-sicko.md`. Keep each role's scope.
- A delegate may not have the parent's catalog or files. Verify that it can read its inputs. If it cannot, provide the exact required source content in its brief or use the host's supported file transfer. A parent-local path alone proves nothing about another executor.

## Discover capabilities before a dependent step

Inspect the actual tools and selected environment. Record what the task needs and what is available. Do not equate the web app with no shell, or a local executor with every local capability.

| Capability | Use when available | When unavailable |
| --- | --- | --- |
| Repository and shell | The actual checkout, Git, and authorized CLI | Read authorized connectors. Mark implementation or command-dependent proof blocked. |
| Subagents and model overrides | Supported launcher fields and current model list | Do not invent a launcher, model field, or concurrency limit. Work inline where a playbook allows it; otherwise record the missing delegation gate. |
| Enforced read-only review | Verified effective sandbox or genuinely read-only tool permissions | A separate instructed reviewer may give advisory findings. It cannot satisfy an enforced read-only gate. |
| Browser or app control | The host's supported browser/computer tool on the required surface | Source inspection cannot replace runtime or visual evidence. Report the exact unverified surface. |
| Durable state and wakeups | Supported task goal, follow-up, event watch, or schedule with a recorded done predicate | Keep available in-task work going. Do not claim an unattended run will survive the turn or restart. Ask for the missing supported route when necessary. |
| Task history | History in context or the authorized reader scoped to this task | Pass a labeled digest. Do not claim a complete transcript audit from a partial digest. |

Local-only syntax in a playbook is an example, not a capability grant. `/goal` means a supported durable task objective with the same scope and done condition. A scheduled follow-up means the actual supported wake mechanism. Preserve the predicate, cadence, ownership, and permission boundaries. If no equivalent exists, record the dependent stage as blocked rather than inventing success. The original playbook's watcher remains the single polling owner when it can run; do not add a competing loop.

Existing connected tools may replace `gh` or `origin` for the same authorized read or write if they expose the required state and action. Keep the selected forge consistent and all head-SHA, blocker, review, and merge gates. A connector that exposes only checks cannot establish merge readiness. Missing CLI semantics remain a gap.

## Model configuration

Read the [setup-owned model contract](../../setup-pstack/references/model-config.md) before selecting models unless the caller supplied a resolved map. Poteto passes the resolved choices and source to children. Local trusted hooks are conveniences; ChatGPT cloud uses explicit skill and configuration reads. Installed resources are not a writable user configuration store.

## Run packaged helpers only on a real executor

Skill-resource reads do not make scripts executable. Use the returned local skill root only on that executor. Otherwise materialize the complete helper subtree through a supported host route into an isolated writable directory, verify every import and required asset, and record the destination. Do not execute text fragments as if they were the full helper.

The original watcher and orchestrator need Bun, their locked package dependencies, and relevant Git/forge access. Orchestrate additionally requires the original Graphite `gt` frontier; verify it before that playbook. Other workflows keep their existing `gh`/Origin selection and do not gain a Graphite requirement. `bootstrap.ts` installs into its scripts directory, so use a writable materialized copy when installed resources are read-only. Do not bundle `node_modules`, install unexpected software, or bypass network restrictions. The plan checker needs Node; the decision logger and worktree audit need their stated shell tools. Check prerequisites before running.

Worktree cleanup also needs evidence that a worktree is not used by an ongoing task. The retained audit is a local helper with its original history assumptions. Do not run its history scan unless that directory is authorized and available on the selected host. Missing or partial history is unknown, not permission to delete. Current task-use evidence remains a separate pruning gate. macOS simulator commands apply only to a verified macOS executor.

## Preserve authority and evidence

The user's request and host policy govern writes, communications, sharing, installs, deletions, and merges. PStack's autonomy language removes needless engineering questions inside that scope; it grants no additional permission. A requested review does not authorize fixes. A requested package does not authorize a GitHub push or PR. When publication is not requested, keep the Opening a PR step with a clear skip reason and deliver the validated artifact.

Report passed, failed, blocked, and never-run stages separately. Count independent read-only review only when enforcement is verified. A worktree separates files, not running processes or permissions. Verification must exercise the same user-facing surface named by the playbook; metadata validation alone is not workflow proof.
