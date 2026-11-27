"""Check export parity and the failure cases that can silently break reuse."""

from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from prompt_package import SECTIONS, read_json, render, validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
PROFILE = read_json(EXAMPLES / "style-profile.json")
TASKS = ("umbrella-repair.json", "speaker-product.json", "library-poster.json")


class PromptPackageTests(unittest.TestCase):
    def test_three_themes_keep_core_and_delivery_in_every_output(self):
        expected_core = {rule["id"] for rule in PROFILE["rules"]}
        for name in TASKS:
            with self.subTest(name=name):
                spec = read_json(EXAMPLES / name)
                outputs = render(spec, PROFILE)
                self.assertEqual(len(outputs), 4)
                zh = json.loads(outputs["prompt.zh.json"])
                en = json.loads(outputs["prompt.en.json"])
                for localized, language in ((zh, "zh"), (en, "en")):
                    self.assertEqual(localized["_meta"]["language"], language)
                    self.assertEqual(set(localized["_meta"]["required_rule_ids"]), expected_core)
                    self.assertEqual(localized["technical"]["delivery"], spec["delivery"])
                    for section in SECTIONS:
                        expected = [
                            {"id": clause["id"], "priority": clause["priority"],
                             "rule_id": clause["rule_id"], "text": clause[language]}
                            for clause in spec["clauses"] if clause["section"] == section
                        ]
                        values = localized[section]
                        if section == "technical":
                            values = values["instructions"]
                        self.assertEqual(values, expected)
                for item in spec["clauses"]:
                    self.assertIn(item["zh"], outputs["prompt.full.zh.txt"])
                    if item["priority"] == "must":
                        self.assertIn(item["zh"], outputs["prompt.short.zh.txt"])
                for name, output in outputs.items():
                    self.assertIn(spec["delivery"]["aspect_ratio"], output)
                    for value in spec["delivery"]["exact_text"]:
                        self.assertIn(value, output, name)

    def test_template_outputs_use_same_placeholders(self):
        spec = read_json(EXAMPLES / "universal-template.json")
        for output in render(spec, PROFILE).values():
            self.assertEqual(set(re.findall(r"\{\{([a-z][a-z0-9_]*)\}\}", output)), set(spec["variables"]))

    def test_translation_omitting_or_duplicating_a_placeholder_fails(self):
        spec = read_json(EXAMPLES / "universal-template.json")
        spec["clauses"][0]["en"] += " {{focus}}"
        with self.assertRaisesRegex(ValueError, "different placeholders"):
            validate(spec, PROFILE)

    def test_unresolved_task_placeholder_fails(self):
        spec = read_json(EXAMPLES / "umbrella-repair.json")
        spec["clauses"][0]["zh"] = "在{{focus}}留下唯一醒目的橙红。"
        with self.assertRaisesRegex(ValueError, "undeclared placeholders"):
            validate(spec, PROFILE)

    def test_missing_core_rule_fails_even_if_task_omits_it_from_its_own_list(self):
        spec = read_json(EXAMPLES / "umbrella-repair.json")
        spec["required_rule_ids"].remove("R03")
        spec["clauses"] = [clause for clause in spec["clauses"] if clause["rule_id"] != "R03"]
        with self.assertRaisesRegex(ValueError, "missing required core rules"):
            validate(spec, PROFILE)

    def test_missing_rule_dependency_fails(self):
        profile = deepcopy(PROFILE)
        profile["rules"][0]["requires"] = ["R04"]
        profile["rules"].append({
            "id": "R04", "category": "style", "priority": "should",
            "variability": "conditional", "requires": [],
        })
        with self.assertRaisesRegex(ValueError, "unapplied dependencies"):
            validate(read_json(EXAMPLES / "umbrella-repair.json"), profile)

    def test_wrong_style_version_fails(self):
        spec = read_json(EXAMPLES / "library-poster.json")
        spec["style_ref"]["version"] = "2.0"
        with self.assertRaisesRegex(ValueError, "version does not match"):
            validate(spec, PROFILE)

    def test_conflicting_exact_text_mode_fails(self):
        spec = read_json(EXAMPLES / "library-poster.json")
        spec["delivery"]["text_mode"] = "none"
        with self.assertRaisesRegex(ValueError, "exact_text list conflicts"):
            validate(spec, PROFILE)

    def test_english_full_version_retains_original_title(self):
        spec = read_json(EXAMPLES / "library-poster.json")
        outputs = render(spec, PROFILE, "en")
        self.assertEqual(len(outputs), 4)
        self.assertIn("雨后阅读日", outputs["prompt.full.en.txt"])
        self.assertIn(spec["clauses"][0]["en"], outputs["prompt.full.en.txt"])
        self.assertIn("prompt.short.zh.txt", outputs)

    def test_sample_exports_match_cli_and_existing_outputs_are_protected(self):
        expected = EXAMPLES / "rendered-library-poster"
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "output"
            command = [
                sys.executable, str(ROOT / "tools" / "prompt_package.py"),
                str(EXAMPLES / "library-poster.json"), "--profile", str(EXAMPLES / "style-profile.json"),
                "--out", str(output),
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertCountEqual([file.name for file in expected.iterdir()], [file.name for file in output.iterdir()])
            for file in expected.iterdir():
                self.assertEqual(file.read_bytes(), (output / file.name).read_bytes())
            result = subprocess.run(command, check=False, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)

    def test_embedded_runtime_json_is_valid_and_prompt_example_compiles(self):
        runtime = (ROOT / "STYLE_CLONE_SYSTEM.md").read_text(encoding="utf-8")
        examples = re.findall(r"```json\n(.*?)\n```", runtime, re.S)
        self.assertEqual(len(examples), 2)
        profile, template = map(json.loads, examples)
        validate(template, profile)


if __name__ == "__main__":
    unittest.main(verbosity=2)
