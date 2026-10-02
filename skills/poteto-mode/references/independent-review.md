# Independent review

For artifact and decision-trail reviews, use a separate subagent session with `fork_turns: "none"`. Self-review does not replace this pass. Prefer Codex agent `pstack-readonly` or an equivalent delegate with an effective read-only sandbox when the launcher supports it. The role name alone does not establish that boundary. When the launcher cannot enforce read-only access, use a separate instruction-only no-write session. Tell it: inspect and report only; do not edit or create files, create commits, push branches, post comments, or run commands that change repository or external state, including outputs and caches. The parent applies any accepted fixes after the review returns.

Record the effective mode as `enforced read-only` or `instruction-only no-write` in the review report. The instruction-only fallback satisfies the separate-review step, but it is not sandbox-enforced isolation. Check the reviewed files and repository status before and after that session; report any unexpected changes and rerun the affected review against the intended artifact. An unchanged artifact is evidence of that run, not proof of enforced isolation. If no separate session is available, report the required review as blocked. These access and reporting rules also apply to `how` explorers and explainers and the Arena judge.

Runtime verifiers use separate sessions with `fork_turns: "none"` and the same model-selection and evidence rules below. Give them only the task-authorized permissions needed to exercise the real app, with isolated outputs. They do not edit the implementation under review. They return verdicts and evidence to the parent, which records ledger rows and publishes authorized PR verdicts.

## Choose the model

Follow the caller's configured reviewer or verifier model and reasoning effort. If an explicit choice is unavailable, report that review as blocked unless the user has authorized a fallback. Without a configured review role, use the parent model at max reasoning. `inherit-parent` and `auto` omit the model override; pass an explicit effort when present, otherwise omit both overrides. Model diversity is optional. Do not choose a less capable model just to change families, or raise the reasoning budget without authorization. Separate sessions on the same model are valid reviews.

## Give the reviewer its own starting point

For an artifact review, provide the task's goal, constraints, artifact, relevant source files, and review criteria. Hold back the author's conclusions and other reviewers' findings until the reviewer records its initial findings. Then provide any rationale or history needed to resolve them. For a decision-trail audit, provide the log and transcript from the start because those are the artifacts under review.

## Check the findings

Require each finding to cite a specific location and supporting evidence, such as a reachable execution path, source text, reproduction, or verification output. Check the evidence before accepting the finding. Agreement can guide further checks but does not prove correctness. Reviewers on the same model can share blind spots. Report reviewer labels, models, and reasoning efforts so separate sessions are not mistaken for model diversity.
