#!/usr/bin/env python3
"""Unit tests for the diff-aware cyclomatic complexity ratchet gate."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

GATE_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "check-complexity.py"))


def make_high_cc_function(name: str = "func", branches: int = 11) -> str:
    """Generate a function with CCN = branches + 1."""
    lines = [f"def {name}(x):"]
    for i in range(branches):
        lines.append(f"    if x == {i}: return {i}")
    lines.append("    return -1\n")
    return "\n".join(lines)


@unittest.skipUnless(shutil.which("lizard"), "lizard CLI is required for complexity ratchet tests")
class TestCheckComplexity(unittest.TestCase):
    """Test suite covering behavior contract of check-complexity.py."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_dir = self.temp_dir.name
        self.git("init")
        self.git("checkout", "-B", "main")
        self.git("config", "user.name", "Complexity Tester")
        self.git("config", "user.email", "tester@example.com")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
            check=check,
        )

    def run_gate(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        return subprocess.run(
            [sys.executable, GATE_SCRIPT, *args],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
            env=run_env,
        )

    def test_new_function_over_limit_fails(self) -> None:
        """A newly introduced function exceeding CCN limit must exit 1."""
        file_path = os.path.join(self.repo_dir, "feature.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("heavy_fn", 11))
        self.git("add", "feature.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 1)
        self.assertIn("complexity: feature.py: heavy_fn( x ) CCN 12 (was new, limit 10)", res.stderr)
        self.assertIn("Split the function", res.stderr)

    def test_legacy_over_limit_untouched_passes(self) -> None:
        """Legacy functions exceeding CCN remain tolerated when untouched."""
        legacy_path = os.path.join(self.repo_dir, "legacy.py")
        with open(legacy_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("legacy_fn", 11))
        self.git("add", "legacy.py")
        self.git("commit", "-m", "Commit legacy code")

        other_path = os.path.join(self.repo_dir, "other.py")
        with open(other_path, "w", encoding="utf-8") as f:
            f.write("def clean_fn():\n    return 42\n")
        self.git("add", "other.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 0, msg=f"Stderr: {res.stderr}")

    def test_legacy_over_limit_made_worse_fails(self) -> None:
        """Making an existing over-limit function more complex must exit 1."""
        file_path = os.path.join(self.repo_dir, "debt.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("debt_fn", 11))
        self.git("add", "debt.py")
        self.git("commit", "-m", "Introduce debt at CCN 12")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("debt_fn", 13))
        self.git("add", "debt.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 1)
        self.assertIn("complexity: debt.py: debt_fn( x ) CCN 14 (was 12, limit 10)", res.stderr)

    def test_legacy_over_limit_improved_passes(self) -> None:
        """Reducing complexity of an over-limit function must pass even if still over limit."""
        file_path = os.path.join(self.repo_dir, "refactor.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("refactor_fn", 15))
        self.git("add", "refactor.py")
        self.git("commit", "-m", "Legacy function with CCN 16")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("refactor_fn", 12))
        self.git("add", "refactor.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 0, msg=f"Stderr: {res.stderr}")

    def test_duplicate_named_functions_regression_fails(self) -> None:
        """Duplicate function names must be paired by rank without collapsing into one dict key."""
        file_path = os.path.join(self.repo_dir, "duplicates.py")
        initial_content = make_high_cc_function("dup_fn", 11) + "\n\n" + make_high_cc_function("dup_fn", 1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(initial_content)
        self.git("add", "duplicates.py")
        self.git("commit", "-m", "Initial duplicate functions (CCN 12 and 2)")

        worse_content = make_high_cc_function("dup_fn", 11) + "\n\n" + make_high_cc_function("dup_fn", 10)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(worse_content)
        self.git("add", "duplicates.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 1)
        self.assertIn("complexity: duplicates.py: dup_fn( x ) CCN 11 (was 2, limit 10)", res.stderr)

    def test_pure_rename_legacy_over_limit_passes(self) -> None:
        """Renaming a file with legacy debt without making it worse must pass."""
        old_path = os.path.join(self.repo_dir, "old_module.py")
        with open(old_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("legacy_fn", 11))
        self.git("add", "old_module.py")
        self.git("commit", "-m", "Add old module")

        self.git("mv", "old_module.py", "new_module.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 0, msg=f"Stderr: {res.stderr}")

    def test_test_file_over_limit_passes(self) -> None:
        """Files matching test naming conventions are exempt by default."""
        test_file = os.path.join(self.repo_dir, "test_service.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("test_complex_matrix", 15))
        self.git("add", "test_service.py")

        tests_dir = os.path.join(self.repo_dir, "tests")
        os.makedirs(tests_dir, exist_ok=True)
        tests_file = os.path.join(tests_dir, "integration.py")
        with open(tests_file, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("helper_fn", 15))
        self.git("add", "tests/integration.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 0, msg=f"Stderr: {res.stderr}")

    def test_ccn_limit_env_override(self) -> None:
        """CCN_LIMIT environment variable overrides default limit."""
        file_path = os.path.join(self.repo_dir, "borderline.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("border_fn", 6))  # CCN = 7
        self.git("add", "borderline.py")

        res_default = self.run_gate()
        self.assertEqual(res_default.returncode, 0)

        res_strict = self.run_gate(env={"CCN_LIMIT": "5"})
        self.assertEqual(res_strict.returncode, 1)
        self.assertIn("complexity: borderline.py: border_fn( x ) CCN 7 (was new, limit 5)", res_strict.stderr)

    def test_base_range_mode(self) -> None:
        """Range mode with --base REF compares against merge-base."""
        base_path = os.path.join(self.repo_dir, "main.py")
        with open(base_path, "w", encoding="utf-8") as f:
            f.write("def entry(): pass\n")
        self.git("add", "main.py")
        self.git("commit", "-m", "Main branch init")

        self.git("checkout", "-b", "feature-branch")
        feat_path = os.path.join(self.repo_dir, "feature.py")
        with open(feat_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("feat_fn", 11))
        self.git("add", "feature.py")
        self.git("commit", "-m", "Feature commit")

        res = self.run_gate("--base", "main")
        self.assertEqual(res.returncode, 1)
        self.assertIn("complexity: feature.py: feat_fn( x ) CCN 12 (was new, limit 10)", res.stderr)

    def test_no_candidate_files_passes(self) -> None:
        """Non-code changes or empty diffs exit 0 without running complexity checks."""
        doc_path = os.path.join(self.repo_dir, "README.md")
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write("# Documentation\n")
        self.git("add", "README.md")

        res = self.run_gate()
        self.assertEqual(res.returncode, 0)

    def test_lizard_missing_with_candidates_fails(self) -> None:
        """When candidate files exist and lizard is not on PATH, exit 2 fail-loud."""
        file_path = os.path.join(self.repo_dir, "code.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("def f(): pass\n")
        self.git("add", "code.py")

        path_without_lizard = os.pathsep.join(
            d for d in os.environ.get("PATH", "").split(os.pathsep)
            if not os.path.exists(os.path.join(d, "lizard"))
        )
        res = self.run_gate(env={"PATH": path_without_lizard})
        self.assertEqual(res.returncode, 2)
        self.assertIn("complexity: lizard not found (pip install lizard)", res.stderr)

    def test_lizard_missing_without_candidates_passes(self) -> None:
        """When no candidate files exist, exit 0 even if lizard is not on PATH."""
        doc_path = os.path.join(self.repo_dir, "notes.txt")
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write("notes\n")
        self.git("add", "notes.txt")

        path_without_lizard = os.pathsep.join(
            d for d in os.environ.get("PATH", "").split(os.pathsep)
            if not os.path.exists(os.path.join(d, "lizard"))
        )
        res = self.run_gate(env={"PATH": path_without_lizard})
        self.assertEqual(res.returncode, 0)

    def test_ccn_exclude_env_override(self) -> None:
        """CCN_EXCLUDE regex skips matching candidate files."""
        file_path = os.path.join(self.repo_dir, "generated_api.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("gen_fn", 11))
        self.git("add", "generated_api.py")

        res = self.run_gate(env={"CCN_EXCLUDE": r"generated_.*\.py"})
        self.assertEqual(res.returncode, 0)

    def test_non_ascii_path_fails(self) -> None:
        """A staged file with non-ASCII characters in path exceeding limit must fail."""
        os.makedirs(os.path.join(self.repo_dir, "src"), exist_ok=True)
        file_path = os.path.join(self.repo_dir, "src", "año.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("def trivial(): return 1\n")
        self.git("add", "src/año.py")
        self.git("commit", "-m", "Initial non-ascii file")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("heavy_fn", 12))  # CCN 13
        self.git("add", "src/año.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 1)
        self.assertIn("src/año.py: heavy_fn( x ) CCN 13", res.stderr)

    def test_rename_from_non_ascii_path_preserves_baseline(self) -> None:
        """Renaming a file from a non-ASCII path preserves baseline debt."""
        os.makedirs(os.path.join(self.repo_dir, "src"), exist_ok=True)
        old_path = os.path.join(self.repo_dir, "src", "año.py")
        with open(old_path, "w", encoding="utf-8") as f:
            f.write(make_high_cc_function("legacy_fn", 12))  # CCN 13
        self.git("add", "src/año.py")
        self.git("commit", "-m", "Initial debt in non-ascii path")

        self.git("mv", "src/año.py", "src/b.py")
        with open(os.path.join(self.repo_dir, "src", "b.py"), "a", encoding="utf-8") as f:
            f.write("\ndef helper(): return 0\n")
        self.git("add", "src/b.py")

        res = self.run_gate()
        self.assertEqual(res.returncode, 0, msg=f"Stderr: {res.stderr}")

    def test_sha256_repository_empty_baseline(self) -> None:
        """Derives empty tree hash dynamically in SHA-256 repositories."""
        sha256_dir = tempfile.TemporaryDirectory()
        try:
            init_res = subprocess.run(
                ["git", "init", "--object-format=sha256"],
                cwd=sha256_dir.name,
                capture_output=True,
                text=True,
            )
            if init_res.returncode != 0:
                self.skipTest("git does not support --object-format=sha256")
            file_path = os.path.join(sha256_dir.name, "mod.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(make_high_cc_function("heavy", 11))
            subprocess.run(["git", "add", "mod.py"], cwd=sha256_dir.name, check=True)
            res_gate = subprocess.run(
                [sys.executable, GATE_SCRIPT, "--base", "HEAD"],
                cwd=sha256_dir.name,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_gate.returncode, 1)
            self.assertIn("mod.py: heavy( x ) CCN 12 (was new, limit 10)", res_gate.stderr)
        finally:
            sha256_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
