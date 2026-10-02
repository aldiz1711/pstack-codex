import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BASELINE = json.loads((ROOT / "tests/fixtures/working-fork-files.json").read_text())
MODEL_NAMES = r"gpt-6(?:\.1)?-(?:luna|astra|sol)|GPT-6(?:\.1)? (?:Luna|Astra|Sol)"
APPROVED_MODEL_NAMES = BASELINE["approved_model_names"]
APPROVED_MAX_DEFAULTS = BASELINE["approved_max_defaults"]
HOST_ONLY = {
    ".codex-plugin/plugin.json", ".codex/agents/comment-sicko.toml", ".codex/agents/poteto-agent.toml",
    ".gitignore", "README.md", "docs/guide/01-setup.md", "skills/how/SKILL.md", "skills/no-comments/SKILL.md",
    "skills/interrogate/SKILL.md", "skills/poteto-mode/playbooks/multi-phase-plan.md",
    "skills/poteto-mode/playbooks/orchestrate.md",
    "skills/poteto-mode/SKILL.md", "skills/setup-pstack/SKILL.md",
}
APPROVED_REVIEW_FALLBACK = {
    "skills/poteto-mode/references/independent-review.md",
    "skills/how/references/explorer-prompt.md",
    "skills/how/references/explainer-prompt.md",
    "skills/interrogate/references/reviewer-prompt.md",
}


class WorkingForkFidelityTests(unittest.TestCase):
    def test_complete_baseline_inventory_is_preserved(self):
        self.assertEqual(BASELINE["baseline"], "ffb1958178011f532a2e1ee2376844120fcc0ce0")
        self.assertEqual(len(BASELINE["files"]), 202)
        for name, expected in BASELINE["files"].items():
            with self.subTest(resource=name):
                file = ROOT / name
                self.assertTrue(file.is_file())
                if name not in HOST_ONLY | APPROVED_REVIEW_FALLBACK | set(APPROVED_MODEL_NAMES) | set(APPROVED_MAX_DEFAULTS):
                    self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), expected["sha256"])
                self.assertEqual(bool(file.stat().st_mode & 0o111), expected["mode"] == "100755")

    def test_unchanged_playbooks_and_helpers_have_no_new_behavior(self):
        original = BASELINE["files"]
        for prefix in ["skills/poteto-mode/playbooks/", "skills/poteto-mode/scripts/"]:
            paths = sorted(path for path in original if path.startswith(prefix))
            self.assertTrue(paths)
            for path in paths:
                if path not in HOST_ONLY | set(APPROVED_MODEL_NAMES):
                    self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), original[path]["sha256"])
        for forbidden in ["host-runtime.md", "model-config.md", "skill-index.json"]:
            self.assertEqual(list((ROOT / "skills").rglob(forbidden)), [])

    def test_review_fallback_preserves_unaffected_policy_and_prompt_text(self):
        regions = {
            "skills/poteto-mode/references/independent-review.md": ([1, 2, 5], "297a03a3e6ac875f7506cebcf151f6d4cb5787187dd740ec1a1937f466fa90f9"),
            "skills/how/references/explorer-prompt.md": ([5], "3a6965276d23be7d8da6c305bfd5d7bf29d2aef09e5dae4119463ac72022a02d"),
            "skills/how/references/explainer-prompt.md": ([11], "aab599104ee487378aad48e2cfab82a2d1f15ae41161891b87c74448b4fcd9f6"),
            "skills/interrogate/references/reviewer-prompt.md": ([15], "6178c9cd023c52fa0bb834a36877cdb3314f1e3c11dd18dc2a454ef7771f46ca"),
        }
        self.assertEqual(set(regions), APPROVED_REVIEW_FALLBACK)
        for path, (changed_blocks, expected) in regions.items():
            with self.subTest(resource=path):
                blocks = (ROOT / path).read_text().split("\n\n")
                unchanged = "\n\n".join(block for index, block in enumerate(blocks) if index not in changed_blocks)
                self.assertEqual(hashlib.sha256(unchanged.encode()).hexdigest(), expected)

    def test_all_skill_models_frontmatter_and_workflow_headings_match(self):
        self.assertEqual(len(BASELINE["skill_contracts"]), 49)
        for path, contract in BASELINE["skill_contracts"].items():
            with self.subTest(skill=path):
                text = (ROOT / path).read_text()
                self.assertEqual(hashlib.sha256(text.split("---", 2)[1].encode()).hexdigest(), contract["frontmatter_sha256"])
                self.assertEqual(re.sub(MODEL_NAMES, "<model>", str(re.findall(r"`gpt-[^`]+`", text))),
                                 re.sub(MODEL_NAMES, "<model>", str(contract["models"])))
                self.assertEqual(re.findall(r"^#{1,6} .+", text, re.MULTILINE), contract["headings"])

    def test_approved_default_edits_preserve_models_and_other_content(self):
        self.assertEqual(len(APPROVED_MODEL_NAMES), 16)
        for path, expected in APPROVED_MODEL_NAMES.items():
            with self.subTest(resource=path):
                text = (ROOT / path).read_text()
                unchanged = re.sub(MODEL_NAMES, "<model>", text)
                approved_hash = APPROVED_MAX_DEFAULTS.get(path, {}).get("non_model_sha256", expected["non_model_sha256"])
                self.assertEqual(hashlib.sha256(unchanged.encode()).hexdigest(), approved_hash)
                self.assertEqual(re.findall(MODEL_NAMES, text), expected["models"])

    def test_inline_default_map_and_panels_without_setup(self):
        text = (ROOT / "skills/setup-pstack/SKILL.md").read_text()
        block = re.search(r"```text\n(.*?)\n```", text, re.DOTALL).group(1)
        roles = {}
        for line in block.splitlines():
            if line.startswith("#"):
                continue
            aliases, choices = line.split(": ", 1)
            entries = [tuple(part.strip() for part in value.split("|")) for value in choices.split(", ")]
            for alias in aliases.split(", "):
                roles[alias] = entries
        for role in ["feature", "refactoring", "bug-fix", "perf-issue", "hillclimb", "how explorer", "why investigators", "swarm workers"]:
            self.assertEqual(roles[role], [("gpt-6.1-sol", "max")])
        for role in ["judgment and prose", "how explainer", "why synthesizer", "reflect tooling", "reflect judgment", "divergent", "synthesizer"]:
            self.assertEqual(roles[role], [("gpt-6.1-sol", "max")])
        self.assertEqual(roles["hardest tasks"], [("gpt-6-astra", "max")])
        self.assertEqual(roles["arena runners"], [("gpt-6.1-sol", "max")] * 4)
        self.assertEqual(roles["architect runners"], [("gpt-6-astra", "max")] * 4)
        for role in ["interrogate reviewers", "arena cross-judge pool"]:
            self.assertEqual(roles[role], [("inherit-parent", "max")])
        self.assertIn("# budget: unlimited (max)", block)

    def test_unlimited_defaults_are_max_across_the_pack(self):
        self.assertEqual(len(APPROVED_MAX_DEFAULTS), 20)
        for path, expected in APPROVED_MAX_DEFAULTS.items():
            with self.subTest(resource=path):
                text = (ROOT / path).read_text()
                self.assertEqual(hashlib.sha256(re.sub(MODEL_NAMES, "<model>", text).encode()).hexdigest(), expected["non_model_sha256"])
                self.assertEqual(re.findall(MODEL_NAMES, text), expected["models"])
        sources = list((ROOT / "skills").rglob("*.md")) + [ROOT / "skills/poteto-mode/scripts/check-plan.mjs"]
        efforts = []
        for path in sources:
            text = path.read_text()
            choices = re.findall(r"`gpt-[^`]+` at (\w+) reasoning", text)
            efforts.extend(choices)
            with self.subTest(resource=str(path.relative_to(ROOT))):
                self.assertTrue(all(effort == "max" for effort in choices))
        self.assertTrue(efforts)
        setup = (ROOT / "skills/setup-pstack/SKILL.md").read_text()
        self.assertIn("`large`, `medium`, and `small` target `xhigh`, `high`, and `medium`", setup)
        self.assertIn("explicit role overrides take precedence", setup)
        self.assertIn("A bare `inherit-parent` or `auto` still inherits both model and effort", setup)

    def test_plan_checker_accepts_default_and_configured_efforts(self):
        text = (ROOT / "skills/poteto-mode/playbooks/multi-phase-plan.md").read_text()
        template = text.split("````markdown\n", 1)[1].split("\n````", 1)[0]
        template = template.replace("independent runtime: separate", "independent runtime with separate")
        checker = ROOT / "skills/poteto-mode/scripts/check-plan.mjs"
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "plan.md"
            for effort in ["max", "xhigh", "high", "medium", "low"]:
                with self.subTest(effort=effort):
                    plan.write_text(template.replace("at max reasoning at the PR head", f"at {effort} reasoning at the PR head"))
                    result = subprocess.run(["node", str(checker), str(plan)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
            for broken in [template.replace("at max reasoning", "at turbo reasoning"),
                           template.replace("- [ ] Lane 10.", "- [ ] Lane 9.")]:
                plan.write_text(broken)
                result = subprocess.run(["node", str(checker), str(plan)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)

    def test_packaged_role_fallbacks_keep_the_original_prompt(self):
        for source, target in [("agents/poteto-agent.md", "skills/poteto-mode/references/poteto-agent.md"),
                               ("agents/comment-sicko.md", "skills/no-comments/references/comment-sicko.md")]:
            self.assertEqual((ROOT / source).read_bytes(), (ROOT / target).read_bytes())

    def test_local_hook_needs_no_map_and_retains_custom_home(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, CODEX_HOME=directory)
            command = [sys.executable, str(ROOT / "hooks/load-pstack-models.py")]
            result = subprocess.run(command, env=env, capture_output=True, text=True, check=True)
            self.assertEqual(result.stdout, "")
            map_file = Path(directory) / "pstack-models.md"
            choices = "# budget: small\nfeature: inherit-parent\nhardest tasks: gpt-6-astra | medium\n"
            map_file.write_text(choices)
            loaded = subprocess.run(command, env=env, capture_output=True, text=True, check=True)
            self.assertTrue(loaded.stdout.endswith(choices))
            self.assertIn("explicit user instructions take precedence", loaded.stdout)
            self.assertEqual(map_file.read_text(), choices)


if __name__ == "__main__":
    unittest.main()
