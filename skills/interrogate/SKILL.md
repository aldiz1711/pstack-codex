---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
---

# Interrogate

Review code changes through separate, read-only sessions under the [independent review policy](../poteto-mode/references/independent-review.md). Each reviewer gets the same prompt and rubric. Reviewers may use the same model. Model diversity is optional.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Determine Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset
- If the user's message references recent work, gather the relevant files

Package the diff (or file contents) plus any surrounding context files the reviewers need to understand the code.

## Step 2, State the Intent

Before spawning reviewers, state the intent explicitly. Derive this from:

- The user's message
- Commit messages
- PR description if one exists
- The code itself

Write one clear paragraph. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Use the `interrogate reviewers` list from `~/.codex/pstack-models.md` when present, one reviewer per entry, including repeated models. Without that line, start with one reviewer on the parent model and effort. Add reviewers when the scope or risk needs more coverage, respecting any count the user requests. Label sessions Reviewer A, B, and so on. Launch them up to the available Codex agent limit, queuing the rest.

For each reviewer:
- use registered Codex agent `pstack-readonly` or an equivalent supported separate reviewer in an effective read-only sandbox under the independent review policy
- configured model and reasoning effort from the `interrogate reviewers` entry, or the parent model and effort with no configured line
- set `fork_turns: "none"` and provide source context without the author's verdict or other reviewers' findings
- pass the same review prompt and rubric

If a configured model or effort is unavailable, report that reviewer as blocked. Use an alternative only when the user has authorized that fallback. Do not silently replace an explicit choice or raise its reasoning budget. If the configured value is `inherit-parent` or `auto`, omit both `model` and `reasoning_effort`. Never treat those aliases as broken slugs.

Read `references/reviewer-prompt.md` and fill in the template with:
1. The stated intent
2. The diff or file contents
3. The review rubric from `references/rubric.md`
4. The code-quality lens from `references/code-quality-review.md`

The same filled template goes to all reviewers, so every model applies the code-quality lens.

## Step 4, Synthesize

As results come back, build a unified picture:

1. **Parse all findings** from the reviewers
2. **Check evidence**. Verify each finding against the code, source, or reproduction before accepting it.
3. **Identify agreement and disagreement**. Record which reviewer labels and models raised each finding. Agreement alone does not establish correctness, especially when reviewers share a model.
4. **Keep supported single-reviewer findings**. A concrete bug does not need another vote.
5. **Deduplicate**. Merge descriptions of the same issue while retaining the evidence and reviewer labels.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework.

Categorize every finding using these buckets:

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact given the current stage.
- **Dismissed**. Wrong, nitpicky, or missing context. Brief explanation why.

For each finding, include:
- Which reviewer labels and models raised it
- The category (act on / consider / noted / dismissed)
- A one-line rationale for the categorization

## Output Format

Present the verdict in this structure:

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [reasoning effort], [N findings] (one bullet per reviewer)

### Act On
[Findings that should be addressed. For each: description, reviewer labels and models, supporting evidence, why it matters.]

### Consider
[Findings worth thinking about. For each: description, reviewer labels and models, supporting evidence, tradeoff involved.]

### Noted
[Valid but low-priority. Brief list.]

### Dismissed
[Rejected findings with brief rationale.]

### Agreement Map
[Where did reviewers agree or disagree? Distinguish separate sessions from model diversity and state what the evidence supports.]
