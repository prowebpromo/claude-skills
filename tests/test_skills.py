"""Offline checks: no credentials or API calls are used by this suite."""
import importlib.util
import json
from pathlib import Path
import re
import unittest
from unittest.mock import Mock, patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "skills_manager", ROOT / "tools/skills-manager/skills_manager.py"
)
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)


class BundledDescriptions(unittest.TestCase):
    def test_json_text_and_yaml_agree(self):
        fixes = json.loads(manager.DEFAULT_FIXES.read_text(encoding="utf-8"))
        self.assertTrue(fixes)
        names, ids = set(), set()
        for fix in fixes:
            with self.subTest(skill=fix["name"]):
                self.assertNotIn(fix["name"], names)
                self.assertNotIn(fix["id"], ids)
                names.add(fix["name"])
                ids.add(fix["id"])
                description = fix["description"]
                self.assertEqual(description, description.strip())
                self.assertTrue(0 < len(description) <= manager.MAX_DESCRIPTION_CHARS)
                self.assertEqual(
                    (ROOT / "fixes" / f'{fix["name"]}.txt').read_text(encoding="utf-8").strip(),
                    description,
                )
                rewritten = manager._replace_description(
                    "---\nname: example\ndescription: old\n---\nBody\n", description
                )
                self.assertEqual(yaml.safe_load(rewritten.split("---", 2)[1])["description"], description)
        self.assertEqual(names, {p.stem for p in (ROOT / "fixes").glob("*.txt")})

    def test_readme_local_links_exist(self):
        for readme in ROOT.rglob("README.md"):
            for target in re.findall(r"\]\(([^)]+)\)", readme.read_text(encoding="utf-8")):
                if "://" not in target and not target.startswith("#"):
                    with self.subTest(readme=str(readme), target=target):
                        self.assertTrue((readme.parent / target.split("#")[0]).exists())


class ManagerLogic(unittest.TestCase):
    def test_replace_preserves_other_metadata_and_body(self):
        original = "---\nname: example\ndescription: >-\n  old description\nmetadata:\n  version: 2\n---\n# Body\n\nKeep this exactly.\n"
        text = 'Quotes: "hello"\nand a second line'
        result = manager._replace_description(original, text)
        meta = yaml.safe_load(result.split("---", 2)[1])
        self.assertEqual(meta, {"name": "example", "description": text, "metadata": {"version": 2}})
        self.assertEqual(result.split("---\n", 2)[2], original.split("---\n", 2)[2])
        self.assertEqual(manager._replace_description(result, text), result)

    def test_missing_frontmatter_fails(self):
        for text in ("# Body", "---\nname: example\n---\nBody"):
            with self.subTest(text=text), self.assertRaises(SystemExit):
                manager._replace_description(text, "new")

    def test_root_skill_selection(self):
        self.assertEqual(manager._skill_md_path({"SKILL.md": b"", "references/SKILL.md": b""}), "SKILL.md")
        self.assertEqual(manager._skill_md_path({"example/SKILL.md": b""}), "example/SKILL.md")
        with self.assertRaises(SystemExit):
            manager._skill_md_path({"example/references/SKILL.md": b""})

    def test_invalid_description_never_downloads(self):
        api = Mock()
        for description in (" ", "x" * 1025):
            with self.subTest(length=len(description)), self.assertRaises(SystemExit):
                manager._update_description(api, "skill_example", description, "1", True)
        api.beta.skills.versions.download.assert_not_called()

    def test_dry_run_never_uploads_and_update_preserves_bundle(self):
        api = Mock()
        files = {"example/SKILL.md": b"---\nname: example\ndescription: old\n---\nBody\n", "example/ref.txt": b"keep"}
        with patch.object(manager, "_download_files", return_value=files.copy()):
            manager._update_description(api, "skill_example", "new", "1", True)
        api.beta.skills.versions.create.assert_not_called()
        with patch.object(manager, "_download_files", return_value=files.copy()):
            manager._update_description(api, "skill_example", "new", "1", False)
        uploaded = dict(api.beta.skills.versions.create.call_args.kwargs["files"])
        self.assertEqual(uploaded["example/ref.txt"], b"keep")
        self.assertTrue(uploaded["example/SKILL.md"].endswith(b"Body\n"))


if __name__ == "__main__":
    unittest.main()
