import importlib.util
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_knowledge", PROJECT_ROOT / "scripts" / "validate_knowledge.py"
)
assert SPEC and SPEC.loader
validate_knowledge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_knowledge)


def write_article(root: Path, relative_path: str, frontmatter: str, body: str = "# Article\n") -> Path:
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"---\n{frontmatter}---\n\n{body}", encoding="utf-8")
    return target


class KnowledgeValidationTests(unittest.TestCase):
    def test_accepts_an_unchanged_legacy_draft_placeholder(self) -> None:
        relative_path = next(iter(validate_knowledge.LEGACY_DRAFT_BASELINE))
        article = PROJECT_ROOT / relative_path

        self.assertEqual(validate_knowledge.validate_paths([article]), [])

    def test_accepts_an_unchanged_migrated_learning_document(self) -> None:
        relative_path = next(iter(validate_knowledge.LEGACY_LEARNING_BASELINE))
        article = PROJECT_ROOT / relative_path

        self.assertEqual(validate_knowledge.validate_paths([article]), [])

    def test_accepts_a_complete_published_article(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = write_article(
                root,
                "02-analyst/structured-discovery.md",
                """id: K-ANALYST-001
title: \"Structured discovery\"
role: analyst
category: methodology
content_type: methodology
difficulty: intermediate
status: published
source_kind: dialogue
evidence_types: [user-confirmed]
related_cases: [CASE-001]
related_demos: []
related_resources: []
date: 2026-08-24
authors: [GoldenTellus]
""",
            )

            self.assertEqual(validate_knowledge.validate_paths([article]), [])

    def test_rejects_a_published_article_missing_required_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = write_article(
                root,
                "02-analyst/missing-metadata.md",
                """id: K-ANALYST-002
title: \"Missing metadata\"
role: analyst
category: methodology
content_type: methodology
difficulty: beginner
status: published
source_kind: dialogue
evidence_types: []
related_cases: []
related_demos: []
related_resources: []
date: 2026-08-24
authors: []
""",
            )

            errors = validate_knowledge.validate_paths([article])

            self.assertTrue(any("author" in error for error in errors), errors)

    def test_rejects_an_article_missing_content_type(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = write_article(
                root,
                "02-analyst/missing-content-type.md",
                """id: K-ANALYST-005
title: "Missing content type"
role: analyst
category: methodology
difficulty: beginner
status: draft
source_kind: dialogue
evidence_types: []
related_cases: []
related_demos: []
related_resources: []
date: 2026-08-25
authors: []
""",
            )

            errors = validate_knowledge.validate_paths([article])

            self.assertTrue(any("content_type" in error for error in errors), errors)

    def test_rejects_duplicate_article_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            frontmatter = """id: K-ANALYST-003
title: \"Duplicate\"
role: analyst
category: methodology
content_type: methodology
difficulty: beginner
status: draft
source_kind: dialogue
evidence_types: []
related_cases: []
related_demos: []
related_resources: []
date: 2026-08-24
authors: []
"""
            write_article(root, "02-analyst/first.md", frontmatter)
            duplicate = write_article(root, "02-analyst/second.md", frontmatter)

            errors = validate_knowledge.validate_paths([root])

            self.assertTrue(any("duplicate ID" in error and str(duplicate) in error for error in errors), errors)

    def test_rejects_an_invalid_calendar_date(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = write_article(
                root,
                "02-analyst/invalid-date.md",
                """id: K-ANALYST-004
title: "Invalid date"
role: analyst
category: methodology
content_type: methodology
difficulty: beginner
status: draft
source_kind: dialogue
evidence_types: []
related_cases: []
related_demos: []
related_resources: []
date: "2026-99-99"
authors: []
""",
            )

            errors = validate_knowledge.validate_paths([article])

            self.assertTrue(any("real calendar date" in error for error in errors), errors)

    def test_accepts_a_case_learning_article_with_a_related_case(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = write_article(
                root,
                "03-architect/rag-tradeoffs.md",
                """id: K-ARCHITECT-001
title: "RAG tradeoffs from a case"
role: architect
category: architecture
content_type: case-learning
difficulty: intermediate
status: draft
source_kind: case
evidence_types: [case-confirmed]
related_cases: [CASE-001]
related_demos: []
related_resources: []
date: 2026-08-25
authors: []
""",
            )

            self.assertEqual(validate_knowledge.validate_paths([article]), [])

    def test_rejects_case_learning_article_without_a_related_case(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = write_article(
                root,
                "03-architect/missing-case.md",
                """id: K-ARCHITECT-002
title: "Missing case link"
role: architect
category: architecture
content_type: case-learning
difficulty: intermediate
status: draft
source_kind: case
evidence_types: [case-confirmed]
related_cases: []
related_demos: []
related_resources: []
date: 2026-08-25
authors: []
""",
            )

            errors = validate_knowledge.validate_paths([article])

            self.assertTrue(any("case-learning articles require" in error for error in errors), errors)

    def test_rejects_case_learning_article_with_a_non_case_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = write_article(
                root,
                "03-architect/wrong-source.md",
                """id: K-ARCHITECT-003
title: "Wrong source kind"
role: architect
category: architecture
content_type: case-learning
difficulty: intermediate
status: draft
source_kind: dialogue
evidence_types: [user-confirmed]
related_cases: [CASE-001]
related_demos: []
related_resources: []
date: 2026-08-25
authors: []
""",
            )

            errors = validate_knowledge.validate_paths([article])

            self.assertTrue(any("source_kind" in error and "case-learning" in error for error in errors), errors)

    def test_rejects_new_draft_placeholder_without_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            placeholder = root / "02-analyst" / "draft.md"
            placeholder.parent.mkdir(parents=True)
            placeholder.write_text("# Draft\n\n状态：待填草稿。\n", encoding="utf-8")

            errors = validate_knowledge.validate_paths([placeholder])

            self.assertTrue(any("frontmatter" in error for error in errors), errors)

    def test_rejects_non_placeholder_article_without_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            article = root / "02-analyst" / "missing-frontmatter.md"
            article.parent.mkdir(parents=True)
            article.write_text("# Article\n\nThis article has no metadata.\n", encoding="utf-8")

            errors = validate_knowledge.validate_paths([article])

            self.assertTrue(any("frontmatter" in error for error in errors))

    def test_ignores_a_repository_migration_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            migration = root / "MIGRATION.md"
            migration.write_text("# Migration\n", encoding="utf-8")

            self.assertEqual(validate_knowledge.validate_paths([root]), [])


if __name__ == "__main__":
    unittest.main()
