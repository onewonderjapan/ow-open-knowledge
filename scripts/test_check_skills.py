#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/check_skills.py の回帰。frontmatter が無い skill はローダから消える。"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = Path(__file__).resolve().parent / "check_skills.py"
SCANNER_PATH = REPO_ROOT / "task-orchestrator" / "scripts" / "scan_skills.py"
PUBLISHED_ROOTS = (
    REPO_ROOT / "cloud-patterns" / "skills",
    REPO_ROOT / "agent-cultivation" / "workbench-skills",
    REPO_ROOT / "task-orchestrator",
    REPO_ROOT / "workflow-standard" / "template",
)
EXPECTED_SKILL_NAMES = frozenset(
    {
        "form-to-cloud-iam",
        "glue-json-rds-merge",
        "homepage-contact-form",
        "terraform-experiment-pitfalls",
        "daily-start",
        "log-outcome",
        "pre-task",
        "retro",
        "weekly-check",
        "task-orchestrator",
        "CHANGE-ME-workflow-name",
    }
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_skill(root: Path, folder: str, frontmatter: str) -> Path:
    skill_dir = root / folder
    skill_dir.mkdir(parents=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(frontmatter, encoding="utf-8")
    return skill_file


class CheckSkillsTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module(MODULE_PATH, "check_skills")
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_repo_published_skills_are_clean(self):
        problems = self.module.check(REPO_ROOT)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_missing_frontmatter_is_rejected(self):
        write_skill(self.root, "deployer", "# deployer\n\nDeploy things.\n")
        problems = self.module.check(self.root)
        self.assertTrue(any("frontmatter" in p for p in problems), problems)

    def test_unclosed_frontmatter_is_rejected(self):
        write_skill(self.root, "deployer", "---\nname: deployer\ndescription: Deploy on incident\n")
        problems = self.module.check(self.root)
        self.assertTrue(any("frontmatter" in p for p in problems), problems)

    def test_missing_description_is_rejected(self):
        write_skill(self.root, "deployer", "---\nname: deployer\n---\n\n# deployer\n")
        problems = self.module.check(self.root)
        self.assertTrue(any("description" in p for p in problems), problems)

    def test_missing_name_is_rejected(self):
        write_skill(
            self.root,
            "deployer",
            "---\ndescription: Deploy on incident\n---\n\n# deployer\n",
        )
        problems = self.module.check(self.root)
        self.assertTrue(any("name" in p for p in problems), problems)

    def test_folded_description_is_accepted(self):
        """Claude Code のよくある `description: >` をローダは受理する。門番もそうであるべき。"""
        write_skill(
            self.root,
            "deployer",
            "---\nname: deployer\ndescription: >\n"
            "  Use when deploying on incident.\n---\n\n# deployer\n",
        )
        self.assertEqual(self.module.check(self.root), [])

    def test_quoted_name_matches_directory(self):
        write_skill(
            self.root,
            "deployer",
            '---\nname: "deployer"\ndescription: Deploy on incident\n---\n\n# deployer\n',
        )
        self.assertEqual(self.module.check(self.root), [])

    def test_explicit_missing_path_fails(self):
        self.assertEqual(self.module.main([str(self.root / "no-such-dir")]), 2)

    def test_explicit_path_with_no_skills_fails(self):
        empty = self.root / "empty-tree"
        empty.mkdir()
        self.assertEqual(self.module.main([str(empty)]), 2)

    def test_short_description_is_rejected(self):
        write_skill(
            self.root,
            "deployer",
            "---\nname: deployer\ndescription: Deploy\n---\n\n# deployer\n",
        )
        problems = self.module.check(self.root)
        self.assertTrue(any("短すぎ" in p for p in problems), problems)

    def test_name_must_match_directory(self):
        write_skill(
            self.root,
            "deployer",
            "---\nname: other-name\ndescription: Deploy on incident\n---\n\n# other\n",
        )
        problems = self.module.check(self.root)
        self.assertTrue(any("一致しません" in p for p in problems), problems)

    def test_placeholder_name_skips_directory_match(self):
        write_skill(
            self.root,
            "template",
            "---\nname: CHANGE-ME-workflow-name\n"
            "description: 一句话说明何时触发、做什么。\n---\n\n# template\n",
        )
        self.assertEqual(self.module.check(self.root), [])

    def test_valid_skill_passes(self):
        write_skill(
            self.root,
            "deployer",
            "---\nname: deployer\ndescription: Deploy on incident\n---\n\n# deployer\n",
        )
        self.assertEqual(self.module.check(self.root), [])


class PublishedSkillCatalogTests(unittest.TestCase):
    """Acceptance: this repo's published skills are catalogable via --root."""

    def test_scan_finds_every_published_skill_via_root(self):
        scanner = load_module(SCANNER_PATH, "scan_skills")
        rules = scanner.load_category_rules(
            REPO_ROOT / "task-orchestrator" / "references" / "category-rules.yaml"
        )
        roots = [("project", path) for path in PUBLISHED_ROOTS]
        result = scanner.scan_roots(roots, rules)
        names = {item["name"] for item in result["skills"]}
        self.assertEqual(result["warnings"], [])
        self.assertEqual(names, EXPECTED_SKILL_NAMES)

    def test_default_scan_of_this_repo_does_not_see_source_packages(self):
        """Published skills are source packages, not installed under .claude/.agents.

        A default scan may still list skills from the user home. What must not
        happen is this repo's published SKILL.md files appearing in that catalog.
        """
        scanner = load_module(SCANNER_PATH, "scan_skills")
        _, roots = scanner.build_default_roots(REPO_ROOT)
        project_paths = [path for scope, path in roots if scope == "project"]
        for published in PUBLISHED_ROOTS:
            self.assertNotIn(published, project_paths)

        rules = scanner.load_category_rules(
            REPO_ROOT / "task-orchestrator" / "references" / "category-rules.yaml"
        )
        result = scanner.scan_roots(roots, rules)
        published_files = {
            path.resolve()
            for root in PUBLISHED_ROOTS
            for path in root.rglob("SKILL.md")
        }
        found_files = {Path(item["skill_file"]).resolve() for item in result["skills"]}
        self.assertFalse(published_files & found_files)


if __name__ == "__main__":
    unittest.main()
