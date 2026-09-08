from __future__ import annotations

import unittest
from pathlib import Path

import generate


ROOT = Path(__file__).resolve().parent
VALID_INVITE = "https://discord.gg/f9GRuKCmRc"
STALE_INVITE = "https://discord.gg/aedatacloud"


class DiscordLinkTest(unittest.TestCase):
    def test_deterministic_profile_uses_valid_invite(self) -> None:
        readme = generate.render_readme([], [], [], [], [])
        self.assertEqual(readme.count(VALID_INVITE), 1)
        self.assertNotIn(STALE_INVITE, readme)

    def test_generated_profile_and_legacy_prompt_have_no_stale_invite(self) -> None:
        self.assertIn(VALID_INVITE, generate.SYSTEM_PROMPT)
        self.assertNotIn(STALE_INVITE, generate.SYSTEM_PROMPT)
        profile = (ROOT / "profile" / "README.md").read_text()
        self.assertIn(VALID_INVITE, profile)
        self.assertNotIn(STALE_INVITE, profile)


if __name__ == "__main__":
    unittest.main()
