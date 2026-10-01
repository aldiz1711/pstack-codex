# PStack cloud-compatibility candidate

This derivative starts from aldiz1711/pstack-codex commit ffb1958178011f532a2e1ee2376844120fcc0ce0. The Git branch and final commit identify the changed source; this baseline pin does not identify a derivative release.

All 49 skills, 23 playbooks, original resources, and MIT notices remain. Local model defaults, hooks, marketplace registration, and manual-only invocation policies are preserved. Added host/resource resolution explicitly supports manual-only sibling reads, cloud configuration loading, and truthful capability gates. The balanced Sol/Astra profile is optional.

`python3 scripts/package-plugin.py` validates the checked-out source. Account export omits the local marketplace registration because a standalone account import accepts one plugin, not a marketplace. Source export retains it. Neither command installs, publishes, tags, or merges anything. The proposed manifest version is a development candidate; no public release or upgrade behavior is claimed.

Lauren Tan created PStack. Zidane Adhitya maintains this unofficial Codex adaptation. Cursor Team Kit supplies the credited control skills. Preserve LICENSE and both licenses/ notices with every distribution.
