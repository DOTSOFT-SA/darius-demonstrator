from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_required_public_files_exist(self) -> None:
        required = [
            ".gitattributes", "README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "THIRD_PARTY_NOTICES.md",
            "browser-edge-client/package-lock.json",
            "CHANGELOG.md", "RELEASE_READINESS.md", ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/feature_request.md", ".github/pull_request_template.md",
            "docs/architecture.md", "docs/data-contract.md", "docs/privacy-and-synthetic-data.md",
            "docs/reproduction-guide.md", "docs/limitations.md",
            "pyproject.toml", "darius_fl_app/client_app.py",
            "darius_fl_app/server_app.py",
            "flower-federated-learning/run_demo.py",
        ]
        self.assertEqual([item for item in required if not (ROOT / item).is_file()], [])

    def test_no_absolute_workspace_paths_in_public_text(self) -> None:
        forbidden = re.compile(r"(?i)([A-Z]:\\Users\\|/home/|/Users/)")
        offenders = []
        excluded_directories = {
            ".venv",
            ".flower-runtime",
            "node_modules",
            "dist",
            "__pycache__",
            ".pytest_cache",
            ".determinism-a",
            ".determinism-b",
            ".tmp-tests",
        }
        for path in ROOT.rglob("*"):
            relative_parts = path.relative_to(ROOT).parts
            if any(part in excluded_directories for part in relative_parts):
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            if path.is_file() and path.suffix.lower() in {".md", ".py", ".js", ".json", ".toml", ".txt", ".example"}:
                if forbidden.search(path.read_text(encoding="utf-8", errors="ignore")):
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
