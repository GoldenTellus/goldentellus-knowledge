"""Validate frontmatter for GoldenTellus knowledge articles."""

from __future__ import annotations

import argparse
import datetime as datetime_module
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml


ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
ALLOWED_STATUSES = {"draft", "review", "published", "archived"}
ALLOWED_SOURCE_KINDS = {"dialogue", "case", "research", "mixed"}
ARTICLE_ID_PATTERN = re.compile(r"^K-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3,}$")
REQUIRED_FIELDS = (
    "id", "title", "role", "category", "difficulty", "status", "source_kind",
    "evidence_types", "related_cases", "related_demos", "related_resources", "date", "authors",
)
LIST_FIELDS = ("evidence_types", "related_cases", "related_demos", "related_resources", "authors")
PLACEHOLDER_MARKER = "状态：待填草稿"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = Path(__file__).with_name("legacy_knowledge_baseline.json")
LEGACY_DRAFT_BASELINE: dict[str, str] = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def load_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Return the YAML mapping in a Markdown file, or a parsing error."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None, None
    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        return None, "frontmatter is missing its closing marker"
    try:
        metadata = yaml.safe_load("\n".join(lines[1:closing_index]))
    except (yaml.YAMLError, ValueError) as error:
        return None, f"frontmatter is not valid YAML: {error}"
    if not isinstance(metadata, dict):
        return None, "frontmatter must be a YAML mapping"
    return metadata, None


def is_baselined_draft_placeholder(path: Path) -> bool:
    """Allow only the unchanged, pre-existing placeholder documents."""
    content = path.read_text(encoding="utf-8")
    if PLACEHOLDER_MARKER not in content:
        return False
    try:
        relative_path = path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return False
    expected_hash = LEGACY_DRAFT_BASELINE.get(relative_path)
    actual_hash = hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    return expected_hash == actual_hash


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def date_as_string(value: Any) -> str | None:
    if isinstance(value, datetime_module.datetime):
        return value.date().isoformat()
    if isinstance(value, datetime_module.date):
        return value.isoformat()
    return value if isinstance(value, str) else None


def validate_article(path: Path) -> list[str]:
    """Validate one article and return errors without raising."""
    metadata, parsing_error = load_frontmatter(path)
    if parsing_error:
        return [f"{path}: {parsing_error}"]
    if metadata is None:
        if is_baselined_draft_placeholder(path):
            return []
        return [f"{path}: article is missing YAML frontmatter"]

    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in metadata:
            errors.append(f"{path}: missing required frontmatter field '{field}'")
    if errors:
        return errors

    identifier = metadata["id"]
    if not is_non_empty_string(identifier) or not ARTICLE_ID_PATTERN.fullmatch(identifier):
        errors.append(f"{path}: id must match K-ROLE-001")
    for field in ("title", "role", "category"):
        if not is_non_empty_string(metadata[field]):
            errors.append(f"{path}: '{field}' must be a non-empty string")
    if metadata["difficulty"] not in ALLOWED_DIFFICULTIES:
        errors.append(f"{path}: difficulty must be one of {sorted(ALLOWED_DIFFICULTIES)}")
    if metadata["status"] not in ALLOWED_STATUSES:
        errors.append(f"{path}: status must be one of {sorted(ALLOWED_STATUSES)}")
    if metadata["source_kind"] not in ALLOWED_SOURCE_KINDS:
        errors.append(f"{path}: source_kind must be one of {sorted(ALLOWED_SOURCE_KINDS)}")
    for field in LIST_FIELDS:
        value = metadata[field]
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{path}: '{field}' must be a list of strings")
    date_value = date_as_string(metadata["date"])
    if not date_value or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value):
        errors.append(f"{path}: date must use YYYY-MM-DD")
    else:
        try:
            datetime_module.date.fromisoformat(date_value)
        except ValueError:
            errors.append(f"{path}: date must be a real calendar date")
    if metadata["status"] == "published" and not metadata["authors"]:
        errors.append(f"{path}: published articles require at least one author")
    return errors


def discover_articles(paths: Iterable[Path]) -> list[Path]:
    articles: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix == ".md" and path.name != "README.md":
            articles.append(path)
        elif path.is_dir():
            articles.extend(item for item in path.rglob("*.md") if item.name != "README.md")
    return sorted(set(articles))


def validate_paths(paths: Iterable[Path]) -> list[str]:
    errors: list[str] = []
    identifiers: dict[str, Path] = {}
    for article in discover_articles(paths):
        errors.extend(validate_article(article))
        metadata, parsing_error = load_frontmatter(article)
        if parsing_error or metadata is None:
            continue
        identifier = metadata.get("id")
        if not isinstance(identifier, str) or "XXX" in identifier:
            continue
        if identifier in identifiers:
            errors.append(f"{article}: duplicate ID {identifier}; first defined in {identifiers[identifier]}")
        else:
            identifiers[identifier] = article
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GoldenTellus knowledge article frontmatter.")
    parser.add_argument("paths", nargs="*", type=Path, default=[Path(".")])
    arguments = parser.parse_args()
    errors = validate_paths(arguments.paths)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("Knowledge frontmatter validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
