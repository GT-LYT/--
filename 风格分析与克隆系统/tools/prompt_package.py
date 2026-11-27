"""Validate one bilingual prompt specification and export four prompt versions."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re


VERSION = "1.0"
SECTIONS = ("style", "character", "environment", "narrative", "mood", "technical")
MODES = ("apply", "expand", "change_theme", "revise")
PRIORITIES = ("must", "should", "may")
VARIABLE_NAME = re.compile(r"[a-z][a-z0-9_]*")
VARIABLE_TOKEN = re.compile(r"\{\{([a-z][a-z0-9_]*)\}\}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def object_fields(value, fields, label):
    require(isinstance(value, dict), f"{label} must be an object")
    missing = set(fields) - value.keys()
    require(not missing, f"{label} missing fields: {', '.join(sorted(missing))}")


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be nonempty text")


def text_array(value, label):
    require(isinstance(value, list), f"{label} must be an array")
    for item in value:
        nonempty(item, label)
    return value


def unique_strings(value, label):
    items = text_array(value, label)
    require(len(items) == len(set(items)), f"{label} contains duplicates")
    return set(items)


def tokens(value, allowed, label):
    names = Counter(VARIABLE_TOKEN.findall(value))
    require(not (names.keys() - allowed), f"{label} contains undeclared placeholders")
    remaining = VARIABLE_TOKEN.sub("", value)
    require("{{" not in remaining and "}}" not in remaining, f"{label} contains malformed placeholders")
    return names


def validate_profile(profile, spec, cited_rules, required_rules):
    object_fields(profile, ("schema_version", "id", "version", "rules"), "style profile")
    require(profile["schema_version"] == VERSION, "unsupported style profile schema")
    require(
        spec["style_ref"] == {"id": profile["id"], "version": profile["version"]},
        "style profile ID or version does not match the task",
    )
    require(isinstance(profile["rules"], list), "style profile rules must be an array")
    rules = {}
    for rule in profile["rules"]:
        object_fields(rule, ("id", "category", "variability", "priority", "requires"), "profile rule")
        nonempty(rule["id"], "profile rule ID")
        require(rule["id"] not in rules, f"duplicate profile rule {rule['id']}")
        require(rule["category"] == "style", f"profile rule {rule['id']} must describe style")
        require(rule["variability"] in ("core", "conditional", "free"), f"invalid variability for {rule['id']}")
        require(rule["priority"] in PRIORITIES, f"invalid priority for {rule['id']}")
        unique_strings(rule["requires"], f"{rule['id']} dependencies")
        rules[rule["id"]] = rule
    unknown = (required_rules | cited_rules) - rules.keys()
    require(not unknown, f"unknown profile rules: {', '.join(sorted(unknown))}")
    must_core = {
        rule_id for rule_id, rule in rules.items()
        if rule["variability"] == "core" and rule["priority"] == "must"
    }
    missing = must_core - required_rules
    require(not missing, f"missing required core rules: {', '.join(sorted(missing))}")
    for rule_id in cited_rules:
        rule = rules[rule_id]
        missing_dependencies = set(rule["requires"]) - cited_rules
        require(not missing_dependencies, f"{rule_id} has unapplied dependencies: {', '.join(sorted(missing_dependencies))}")
        if rule["priority"] == "must":
            require(rule_id in required_rules, f"applied must rule {rule_id} is not mandatory in the task")


def validate(spec, profile=None):
    fields = (
        "schema_version", "package_kind", "task_id", "mode", "style_ref",
        "required_rule_ids", "variables", "delivery", "clauses",
    )
    object_fields(spec, fields, "prompt specification")
    require(spec["schema_version"] == VERSION, "unsupported prompt specification schema")
    require(spec["package_kind"] in ("template", "task"), "invalid package_kind")
    require(spec["mode"] in MODES, "invalid mode")
    nonempty(spec["task_id"], "task_id")
    object_fields(spec["style_ref"], ("id", "version"), "style_ref")
    for key in ("id", "version"):
        nonempty(spec["style_ref"][key], f"style_ref.{key}")
    allowed = unique_strings(spec["variables"], "variables")
    require(all(VARIABLE_NAME.fullmatch(name) for name in allowed), "invalid variable name")
    if spec["package_kind"] == "task":
        require(not allowed, "task packages must resolve all variables")

    delivery = spec["delivery"]
    object_fields(delivery, ("aspect_ratio", "quantity", "format", "text_mode", "exact_text"), "delivery")
    ratio = delivery["aspect_ratio"]
    if ratio is not None:
        require(isinstance(ratio, str) and re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", ratio), "invalid aspect ratio")
    quantity = delivery["quantity"]
    require(type(quantity) is int and quantity >= 1, "quantity must be a positive integer")
    if delivery["format"] is not None:
        nonempty(delivery["format"], "delivery.format")
        tokens(delivery["format"], set(), "delivery.format")
    text_mode = delivery["text_mode"]
    require(text_mode in ("none", "exact", "unspecified"), "invalid text_mode")
    exact_text = text_array(delivery["exact_text"], "exact_text")
    require(bool(exact_text) == (text_mode == "exact"), "exact_text list conflicts with text_mode")
    used = set()
    for value in exact_text:
        used.update(tokens(value, allowed, "exact_text"))

    required_rules = unique_strings(spec["required_rule_ids"], "required_rule_ids")
    require(bool(required_rules), "include at least one mandatory style rule")
    clauses = spec["clauses"]
    require(isinstance(clauses, list) and bool(clauses), "clauses must be a nonempty array")
    clause_ids = set()
    cited_rules = set()
    exposed_required_rules = set()
    has_mandatory_subject = False
    for clause in clauses:
        object_fields(clause, ("id", "section", "priority", "rule_id", "zh", "en"), "clause")
        clause_id = clause["id"]
        nonempty(clause_id, "clause ID")
        require(clause_id not in clause_ids, f"duplicate clause ID {clause_id}")
        clause_ids.add(clause_id)
        section = clause["section"]
        priority = clause["priority"]
        require(section in SECTIONS, f"{clause_id} has an invalid section")
        require(priority in PRIORITIES, f"{clause_id} has an invalid priority")
        for language in ("zh", "en"):
            nonempty(clause[language], f"{clause_id}.{language}")
        zh_tokens = tokens(clause["zh"], allowed, f"{clause_id}.zh")
        en_tokens = tokens(clause["en"], allowed, f"{clause_id}.en")
        require(zh_tokens == en_tokens, f"{clause_id} has different placeholders across languages")
        used.update(zh_tokens)
        rule_id = clause["rule_id"]
        if rule_id is not None:
            nonempty(rule_id, f"{clause_id}.rule_id")
            require(section == "style", f"{clause_id} must place style rule references in style")
            cited_rules.add(rule_id)
            if priority == "must":
                exposed_required_rules.add(rule_id)
        if section == "character" and priority == "must":
            has_mandatory_subject = True
    require(has_mandatory_subject, "include a mandatory subject in character")
    require(used == allowed, f"unused declared placeholders: {', '.join(sorted(allowed - used))}")
    require(exposed_required_rules == required_rules, "required_rule_ids must match style clauses with must priority")
    if profile is not None:
        validate_profile(profile, spec, cited_rules, required_rules)


def localized_json(spec, language):
    output = {
        "_meta": {
            key: spec[key]
            for key in ("schema_version", "package_kind", "task_id", "mode", "style_ref", "required_rule_ids", "variables")
        }
    }
    output["_meta"]["language"] = language
    for section in SECTIONS:
        items = [
            {
                "id": clause["id"],
                "priority": clause["priority"],
                "rule_id": clause["rule_id"],
                "text": clause[language],
            }
            for clause in spec["clauses"]
            if clause["section"] == section
        ]
        if section == "technical":
            output[section] = {"delivery": spec["delivery"], "instructions": items}
        else:
            output[section] = items
    return json.dumps(output, ensure_ascii=False, indent=2) + "\n"


def delivery_text(delivery, language):
    quantity = delivery["quantity"]
    ratio = delivery["aspect_ratio"]
    output_format = delivery["format"]
    separator = "、" if language == "zh" else ", "
    exact = separator.join(json.dumps(value, ensure_ascii=False) for value in delivery["exact_text"])
    if language == "zh":
        text = [f"输出{quantity}张图。"]
        if ratio:
            text.append(f"画幅比例为 {ratio}。")
        if output_format:
            text.append(f"输出格式为 {output_format}。")
        if delivery["text_mode"] == "none":
            text.append("画面无文字。")
        elif delivery["text_mode"] == "exact":
            text.append(f"图中文字严格使用以下原文 {exact}。")
        return "".join(text)
    text = [f"Deliver {quantity} image(s)."]
    if ratio:
        text.append(f"Use an aspect ratio of {ratio}.")
    if output_format:
        text.append(f"Deliver in {output_format} format.")
    if delivery["text_mode"] == "none":
        text.append("The image must contain no text.")
    elif delivery["text_mode"] == "exact":
        text.append(f"Use the following exact text in the image: {exact}.")
    return " ".join(text)


def natural_text(spec, language, short=False):
    separator = "" if language == "zh" else " "
    groups = []
    for section in SECTIONS:
        parts = [
            clause[language].strip()
            for clause in spec["clauses"]
            if clause["section"] == section and (not short or clause["priority"] == "must")
        ]
        if parts:
            groups.append(separator.join(parts))
    groups.append(delivery_text(spec["delivery"], language))
    return (separator if short else "\n\n").join(groups) + "\n"


def render(spec, profile=None, full_language="zh"):
    require(full_language in ("zh", "en"), "invalid language for full prompt")
    validate(spec, profile)
    return {
        "prompt.zh.json": localized_json(spec, "zh"),
        "prompt.en.json": localized_json(spec, "en"),
        "prompt.short.zh.txt": natural_text(spec, "zh", short=True),
        f"prompt.full.{full_language}.txt": natural_text(spec, full_language),
    }


def read_json(path):
    def disallow_duplicates(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key {key}")
            result[key] = value
        return result

    def disallow_nonstandard_number(value):
        raise ValueError(f"invalid JSON number {value}")

    with path.open(encoding="utf-8-sig") as stream:
        return json.load(
            stream,
            object_pairs_hook=disallow_duplicates,
            parse_constant=disallow_nonstandard_number,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="path to the prompt specification JSON")
    parser.add_argument("--profile", type=Path, help="check rule IDs and version against the style profile")
    parser.add_argument("--out", type=Path, help="write the four prompt variants to a new directory")
    parser.add_argument("--full-language", choices=("zh", "en"), default="zh")
    args = parser.parse_args()
    try:
        spec = read_json(args.spec)
        profile = read_json(args.profile) if args.profile else None
        files = render(spec, profile, args.full_language)
        if args.out:
            args.out.mkdir(parents=True, exist_ok=False)
            written = []
            try:
                for name, text in files.items():
                    path = args.out / name
                    with path.open("x", encoding="utf-8", newline="\n") as stream:
                        written.append(path)
                        stream.write(text)
            except OSError:
                for path in written:
                    path.unlink(missing_ok=True)
                if not any(args.out.iterdir()):
                    args.out.rmdir()
                raise
            print(f"Exported four prompt variants to {args.out}")
        else:
            print("Prompt specification validated")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
