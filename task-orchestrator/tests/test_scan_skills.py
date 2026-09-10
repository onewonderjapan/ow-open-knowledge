import importlib.util
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = SKILL_ROOT / "scripts" / "scan_skills.py"


def load_module():
    spec = importlib.util.spec_from_file_location("scan_skills", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_skill(root: Path, folder: str, name: str, description: str) -> Path:
    skill_dir = root / folder
    skill_dir.mkdir(parents=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    return skill_file


class ScanSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.rules_file = self.root / "category-rules.yaml"
        self.rules_file.write_text(
            "categories:\n"
            "  frontend:\n"
            "    - react\n"
            "    - ui\n"
            "  sre:\n"
            "    - deploy\n"
            "    - incident\n"
            "  excel:\n"
            "    - excel\n"
            "    - csv\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_classifies_one_skill_into_multiple_categories(self):
        module = load_module()
        skill_file = write_skill(
            self.root, "react-deploy", "react-deploy", "Deploy a React UI safely"
        )
        result = module.scan_roots(
            [("project", self.root)], module.load_category_rules(self.rules_file)
        )
        record = next(
            item for item in result["skills"] if item["skill_file"] == str(skill_file)
        )
        self.assertEqual(record["categories"], ["frontend", "sre"])
        self.assertTrue(record["writable"])

    def test_keeps_same_name_at_different_paths(self):
        module = load_module()
        first = self.root / "first"
        second = self.root / "second"
        write_skill(first, "shared", "shared", "React UI work")
        write_skill(second, "shared", "shared", "Excel workbook work")
        result = module.scan_roots(
            [("project", first), ("user", second)],
            module.load_category_rules(self.rules_file),
        )
        self.assertEqual(
            [item["name"] for item in result["skills"]], ["shared", "shared"]
        )
        self.assertEqual(
            [item["scope"] for item in result["skills"]], ["project", "user"]
        )

    def test_deduplicates_symlinked_physical_file(self):
        module = load_module()
        source = self.root / "source"
        linked = self.root / "linked"
        write_skill(source, "one", "one", "React UI work")
        linked.symlink_to(source, target_is_directory=True)
        result = module.scan_roots(
            [("user", source), ("user", linked)],
            module.load_category_rules(self.rules_file),
        )
        self.assertEqual(len(result["skills"]), 1)

    def test_reports_malformed_frontmatter_and_continues(self):
        module = load_module()
        bad_dir = self.root / "bad"
        bad_dir.mkdir()
        (bad_dir / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
        good = write_skill(self.root, "good", "good", "CSV processing")
        result = module.scan_roots(
            [("project", self.root)], module.load_category_rules(self.rules_file)
        )
        self.assertEqual(
            [item["skill_file"] for item in result["skills"]], [str(good)]
        )
        self.assertEqual(len(result["warnings"]), 1)

    def test_marks_protected_scopes_read_only(self):
        module = load_module()
        write_skill(self.root, "protected", "protected", "Incident response")
        for scope in ("plugin", "admin", "system"):
            result = module.scan_roots(
                [(scope, self.root)], module.load_category_rules(self.rules_file)
            )
            self.assertFalse(result["skills"][0]["writable"])

    def test_unmatched_skill_uses_other(self):
        module = load_module()
        write_skill(self.root, "novel", "novel", "Quantum lattice analysis")
        result = module.scan_roots(
            [("user", self.root)], module.load_category_rules(self.rules_file)
        )
        self.assertEqual(result["skills"][0]["categories"], ["other"])

    def test_empty_root_returns_empty_catalog(self):
        module = load_module()
        result = module.scan_roots(
            [("project", self.root)], module.load_category_rules(self.rules_file)
        )
        self.assertEqual(result["skills"], [])
        self.assertEqual(result["warnings"], [])

    def test_parses_folded_description(self):
        module = load_module()
        skill_dir = self.root / "folded"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            "---\nname: folded\ndescription: >\n  Use when working with React\n"
            "  user interfaces.\n---\n\n# Folded\n",
            encoding="utf-8",
        )
        parsed = module.parse_skill(skill_file)
        self.assertEqual(
            parsed["description"], "Use when working with React user interfaces."
        )

    def test_default_roots_use_cwd_when_outside_git(self):
        module = load_module()
        cwd = self.root / "plain-directory"
        cwd.mkdir()
        project_root, roots = module.build_default_roots(cwd)
        self.assertEqual(project_root, cwd.resolve())
        self.assertIn(("project", cwd / ".agents" / "skills"), roots)


if __name__ == "__main__":
    unittest.main()
