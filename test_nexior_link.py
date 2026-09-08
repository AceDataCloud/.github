from __future__ import annotations

import unittest
from pathlib import Path

import generate


ROOT = Path(__file__).resolve().parent


class NexiorLinkTest(unittest.TestCase):
    def test_deterministic_profile_uses_canonical_studio_url(self) -> None:
        readme = generate.render_readme([], [], [], [], [])
        self.assertEqual(readme.count("https://studio.acedata.cloud"), 2)
        self.assertNotIn("hub.acedata.cloud", readme)

    def test_generated_profile_and_legacy_prompt_have_no_retired_url(self) -> None:
        self.assertNotIn("hub.acedata.cloud", generate.SYSTEM_PROMPT)
        self.assertNotIn("hub.acedata.cloud", (ROOT / "profile" / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
