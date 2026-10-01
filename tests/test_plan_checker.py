from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


@unittest.skipUnless(shutil.which("node"), "the plan checker requires Node")
class PlanCheckerTests(unittest.TestCase):
    def skeleton(self):
        source = (ROOT / "skills/poteto-mode/playbooks/multi-phase-plan.md").read_text()
        return source.split("````markdown\n", 1)[1].split("\n````", 1)[0]

    def check(self, text):
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "plan.md"
            plan.write_text(text)
            return subprocess.run(
                ["node", str(ROOT / "skills/poteto-mode/scripts/check-plan.mjs"), str(plan)],
                capture_output=True, text=True,
            )

    def test_current_skeleton_satisfies_the_real_checker(self):
        result = self.check(self.skeleton())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 PR sections, 0 problems", result.stdout)
        self.assertIn("verify-live=10", result.stdout)

    def test_missing_lane_still_fails_the_ten_lane_gate(self):
        text = self.skeleton()
        text = "\n".join(line for line in text.splitlines() if not line.startswith("- [ ] Lane 10."))
        result = self.check(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected 1 to 10", result.stderr)

    def test_plan_cannot_hardcode_the_old_luna_fallback(self):
        text = self.skeleton().replace(
            "Ten lanes using the resolved `swarm workers` role at the PR head",
            "Ten lanes on `gpt-6-luna` at xhigh reasoning at the PR head",
        )
        result = self.check(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Verify, live lacks", result.stderr)


if __name__ == "__main__":
    unittest.main()
