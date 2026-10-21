#!/usr/bin/env python3
"""Diff-aware cyclomatic-complexity ratchet gate.

Blocks commits that introduce a function exceeding the CCN limit or worsen an
already over-limit function, while untouched legacy debt passes.
"""

import argparse
import csv
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Optional, Pattern

SUPPORTED_EXTENSIONS = (
    ".kt", ".kts", ".go", ".py", ".java",
    ".js", ".jsx", ".ts", ".tsx", ".rs",
    ".c", ".cc", ".cpp", ".h", ".hpp",
    ".swift", ".rb", ".php", ".cs", ".scala",
)

DEFAULT_EXCLUDE_RE = re.compile(
    r"(?:^|/)(?:build|vendor|node_modules|test|tests|androidTest)(?:/|$)"
    r"|.*_test\.go$"
    r"|.*Tests?\.kt$"
    r"|(?:^|/)test_[^/]*\.py$"
    r"|.*_test\.py$"
    r"|\.(?:spec|test)\."
)

GIT_ENV = {**os.environ, "LC_ALL": "C"}


def git_cmd(*args: str) -> str:
    """Run a git command with LC_ALL=C, surfacing any failure immediately."""
    res = subprocess.run(["git", *args], capture_output=True, text=True, env=GIT_ENV)
    if res.returncode != 0:
        raise subprocess.CalledProcessError(res.returncode, ["git", *args], res.stdout, res.stderr)
    return res.stdout


def has_head() -> bool:
    """Check whether HEAD exists in the current git repository."""
    res = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], capture_output=True, text=True, env=GIT_ENV)
    return res.returncode == 0


def is_merging() -> bool:
    """Check whether a merge is in progress via MERGE_HEAD.

    Note: Octopus merges use only the first MERGE_HEAD ref since .git internals
    are off-limits and git rev-parse resolves the primary merge head.
    """
    res = subprocess.run(["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"], capture_output=True, env=GIT_ENV)
    return res.returncode == 0


def get_merge_base(ref: str) -> str:
    """Compute the merge-base between a target ref and HEAD."""
    return git_cmd("merge-base", ref, "HEAD").strip()


def get_empty_tree_hash() -> str:
    """Return the empty tree hash derived dynamically for the repository."""
    return git_cmd("hash-object", "-t", "tree", "/dev/null").strip()


def ref_path_exists(ref: str, path: str) -> bool:
    """Check whether a path exists in the given git ref."""
    res = subprocess.run(["git", "cat-file", "-e", f"{ref}:{path}"], capture_output=True, env=GIT_ENV)
    return res.returncode == 0


def get_file_at_ref(ref: str, path: str) -> str:
    """Fetch file content at ref, returning empty string if missing."""
    if not ref_path_exists(ref, path):
        return ""
    return git_cmd("show", f"{ref}:{path}")


def get_limit() -> int:
    """Return CCN limit from CCN_LIMIT env var, defaulting to 10."""
    val = os.environ.get("CCN_LIMIT", "").strip()
    return int(val) if val else 10


def get_exclude_pattern() -> Optional[Pattern[str]]:
    """Return extra exclusion pattern from CCN_EXCLUDE env var if configured."""
    pattern = os.environ.get("CCN_EXCLUDE", "").strip()
    return re.compile(pattern) if pattern else None


def is_candidate_file(path: str, extra_pattern: Optional[Pattern[str]] = None) -> bool:
    """Check if a file matches supported code extensions and is not excluded."""
    if not path.endswith(SUPPORTED_EXTENSIONS):
        return False
    if DEFAULT_EXCLUDE_RE.search(path):
        return False
    if extra_pattern:
        return not bool(extra_pattern.search(path))
    return True


def parse_next_record(tokens: list[str], idx: int) -> tuple[tuple[str, str, Optional[str]], int]:
    """Parse next record from NUL-separated diff tokens."""
    status = tokens[idx]
    if status.startswith(("R", "C")):
        return (status, tokens[idx + 2], tokens[idx + 1]), idx + 3
    old_path = tokens[idx + 1] if status.startswith(("M", "D")) else None
    return (status, tokens[idx + 1], old_path), idx + 2


def parse_z_diff(raw_diff: str) -> list[tuple[str, str, Optional[str]]]:
    """Parse git diff -z NUL-separated records."""
    tokens = raw_diff.split("\0")
    records = []
    idx = 0
    while idx + 1 < len(tokens):
        if not tokens[idx]:
            break
        record, idx = parse_next_record(tokens, idx)
        records.append(record)
    return records


def get_raw_diff(base_ref: Optional[str], is_staged: bool) -> str:
    """Retrieve raw name-status diff from git with -z."""
    if is_staged:
        return git_cmd("diff", "--cached", "--name-status", "-M", "--diff-filter=AMRD", "-z")
    target_ref = base_ref if base_ref else get_empty_tree_hash()
    return git_cmd("diff", "--name-status", "-M", "--diff-filter=AMRD", "-z", target_ref)


def is_analysis_candidate(record: tuple[str, str, Optional[str]], extra_exclude: Optional[Pattern[str]]) -> bool:
    """Check if record represents an active source file requiring complexity analysis."""
    if record[0].startswith("D"):
        return False
    return is_candidate_file(record[1], extra_exclude)


def collect_candidates(
    records: list[tuple[str, str, Optional[str]]],
    extra_exclude: Optional[Pattern[str]],
) -> list[tuple[str, str, Optional[str]]]:
    """Collect candidate files requiring complexity analysis."""
    candidates = []
    for record in records:
        if is_analysis_candidate(record, extra_exclude):
            candidates.append(record)
    return candidates


def parse_lizard_csv(csv_text: str) -> dict[str, list[int]]:
    """Parse lizard CSV output into mapping of function long_name to CCN list."""
    functions: dict[str, list[int]] = {}
    for row in csv.reader(io.StringIO(csv_text)):
        if len(row) > 8:
            functions.setdefault(row[8], []).append(int(row[1]))
    return functions


def analyze_source(source: str, suffix: str) -> dict[str, list[int]]:
    """Analyze source code with lizard using a temporary file with the original extension."""
    if not source:
        return {}
    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.write(source)
        res = subprocess.run(["lizard", "--csv", tmp_path], capture_output=True, text=True, check=True)
        return parse_lizard_csv(res.stdout)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def previous_ccn(old_ccn: Optional[int]) -> tuple[int, str]:
    """Convert optional old CCN into baseline value and display string."""
    if old_ccn is None:
        return 0, "new"
    return old_ccn, str(old_ccn)


def violation_for_pair(
    path: str,
    name: str,
    new_ccn: int,
    old_ccn: Optional[int],
    limit: int,
) -> Optional[str]:
    """Return formatted violation message if new CCN exceeds limit and previous CCN."""
    prev_ccn, was = previous_ccn(old_ccn)
    if new_ccn > limit and new_ccn > prev_ccn:
        return f"{path}: {name} CCN {new_ccn} (was {was}, limit {limit})"
    return None


def check_function_violations(
    path: str,
    name: str,
    new_ccns: list[int],
    old_ccns: list[int],
    limit: int,
) -> list[str]:
    """Pair new and baseline CCNs by rank and detect ratchet violations."""
    sorted_new = sorted(new_ccns, reverse=True)
    sorted_old = sorted(old_ccns, reverse=True)
    padded_old: list[Optional[int]] = list(sorted_old) + [None] * max(0, len(sorted_new) - len(sorted_old))
    violations = []
    for new_val, old_val in zip(sorted_new, padded_old):
        msg = violation_for_pair(path, name, new_val, old_val, limit)
        if msg:
            violations.append(msg)
    return violations


def read_source(path: str, is_staged: bool) -> str:
    """Read new source from git index in staged mode or working tree in range mode."""
    if is_staged:
        return git_cmd("show", f":{path}")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def read_baseline_source(status: str, old_path: Optional[str], base_ref: Optional[str]) -> str:
    """Read baseline source for modified or renamed files."""
    if status.startswith("A") or not base_ref or not old_path:
        return ""
    return get_file_at_ref(base_ref, old_path)


def is_pool_candidate_record(
    old_path: Optional[str],
    base_ref: Optional[str],
    extra_exclude: Optional[Pattern[str]],
) -> bool:
    """Check if record can contribute moved-out baseline functions."""
    if not base_ref or not old_path:
        return False
    return is_candidate_file(old_path, extra_exclude)


def get_new_function_names(
    status: str,
    path: str,
    is_staged: bool,
    extra_exclude: Optional[Pattern[str]],
) -> set[str]:
    """Return names of functions present in the new version of a candidate file."""
    if status.startswith("D") or not is_candidate_file(path, extra_exclude):
        return set()
    suffix = os.path.splitext(path)[1]
    new_src = read_source(path, is_staged)
    return set(analyze_source(new_src, suffix).keys())


def record_moved_out_functions(
    record: tuple[str, str, Optional[str]],
    base_ref: str,
    is_staged: bool,
    extra_exclude: Optional[Pattern[str]],
) -> dict[str, list[int]]:
    """Extract baseline functions from a record that no longer exist in its new version."""
    status, path, old_path = record
    if not is_pool_candidate_record(old_path, base_ref, extra_exclude):
        return {}
    assert old_path is not None
    old_suffix = os.path.splitext(old_path)[1]
    before = analyze_source(read_baseline_source(status, old_path, base_ref), old_suffix)
    new_names = get_new_function_names(status, path, is_staged, extra_exclude)
    return {name: ccns for name, ccns in before.items() if name not in new_names}


def build_moved_out_pool(
    records: list[tuple[str, str, Optional[str]]],
    base_ref: Optional[str],
    is_staged: bool,
    extra_exclude: Optional[Pattern[str]],
) -> dict[str, list[int]]:
    """Build pool of moved-out functions from candidate records, sorted by CCN descending."""
    if not base_ref:
        return {}
    pool: dict[str, list[int]] = {}
    for record in records:
        for name, ccns in record_moved_out_functions(record, base_ref, is_staged, extra_exclude).items():
            pool.setdefault(name, []).extend(ccns)
    for ccns in pool.values():
        ccns.sort(reverse=True)
    return pool


def check_fallback_violations(
    path: str,
    name: str,
    new_ccns: list[int],
    pool: dict[str, list[int]],
    limit: int,
) -> list[str]:
    """Pair new CCNs with consumed pool entries by rank and detect ratchet violations."""
    violations = []
    for new_val in sorted(new_ccns, reverse=True):
        old_val = pool[name].pop(0) if pool.get(name) else None
        msg = violation_for_pair(path, name, new_val, old_val, limit)
        if msg:
            violations.append(msg)
    return violations


def check_name_violations(
    path: str,
    name: str,
    new_ccns: list[int],
    before: dict[str, list[int]],
    pool: dict[str, list[int]],
    limit: int,
) -> list[str]:
    """Check violations using same-file baseline if present, or pool fallback if absent."""
    if name in before:
        return check_function_violations(path, name, new_ccns, before[name], limit)
    return check_fallback_violations(path, name, new_ccns, pool, limit)


def combine_ccn_lists(list_a: list[int], list_b: list[int]) -> list[int]:
    """Combine two CCN lists by rank-pairing descending and taking element-wise max."""
    sorted_a = sorted(list_a, reverse=True)
    sorted_b = sorted(list_b, reverse=True)
    min_len = min(len(sorted_a), len(sorted_b))
    paired = [max(sorted_a[i], sorted_b[i]) for i in range(min_len)]
    return paired + sorted_a[min_len:] + sorted_b[min_len:]


def combine_parent_baselines(
    head_fns: dict[str, list[int]],
    merge_fns: dict[str, list[int]],
) -> dict[str, list[int]]:
    """Combine baseline functions from HEAD and MERGE_HEAD taking element-wise max."""
    all_names = set(head_fns.keys()) | set(merge_fns.keys())
    combined: dict[str, list[int]] = {}
    for name in all_names:
        combined[name] = combine_ccn_lists(head_fns.get(name, []), merge_fns.get(name, []))
    return combined


def get_merge_candidate_paths(status: str, path: str, old_path: Optional[str]) -> list[str]:
    """Return ordered list of candidate paths in MERGE_HEAD."""
    if status.startswith(("R", "C")) and old_path:
        return [old_path, path]
    return [path]


def resolve_merge_head_path(status: str, path: str, old_path: Optional[str]) -> Optional[str]:
    """Determine path in MERGE_HEAD, trying old then new path for renames."""
    for candidate in get_merge_candidate_paths(status, path, old_path):
        if ref_path_exists("MERGE_HEAD", candidate):
            return candidate
    return None


def read_merge_baseline_functions(
    status: str,
    path: str,
    old_path: Optional[str],
) -> dict[str, list[int]]:
    """Analyze file at MERGE_HEAD if present."""
    merge_path = resolve_merge_head_path(status, path, old_path)
    if not merge_path:
        return {}
    merge_src = get_file_at_ref("MERGE_HEAD", merge_path)
    suffix = os.path.splitext(merge_path)[1]
    return analyze_source(merge_src, suffix)


def resolve_file_baseline(
    status: str,
    path: str,
    old_path: Optional[str],
    base_ref: Optional[str],
    merging: bool,
) -> dict[str, list[int]]:
    """Resolve baseline functions for candidate file from base_ref and MERGE_HEAD if merging."""
    old_src = read_baseline_source(status, old_path, base_ref)
    suffix = os.path.splitext(old_path)[1] if old_path else os.path.splitext(path)[1]
    head_fns = analyze_source(old_src, suffix)
    if not merging:
        return head_fns
    merge_fns = read_merge_baseline_functions(status, path, old_path)
    return combine_parent_baselines(head_fns, merge_fns)


def file_violations(
    status: str,
    path: str,
    old_path: Optional[str],
    base_ref: Optional[str],
    is_staged: bool,
    limit: int,
    pool: dict[str, list[int]],
    merging: bool = False,
) -> list[str]:
    """Calculate complexity violations for a candidate file."""
    new_src = read_source(path, is_staged)
    suffix = os.path.splitext(path)[1]
    after = analyze_source(new_src, suffix)
    before = resolve_file_baseline(status, path, old_path, base_ref, merging)
    violations = []
    for name, new_ccns in after.items():
        violations.extend(check_name_violations(path, name, new_ccns, before, pool, limit))
    return violations


def resolve_baseline(base_arg: Optional[str]) -> tuple[Optional[str], bool]:
    """Determine the baseline reference and whether staged mode applies."""
    if not has_head():
        return None, base_arg is None
    if base_arg:
        return get_merge_base(base_arg), False
    return "HEAD", True


def report_violations(violations: list[str]) -> int:
    """Print violations and remediation advice to stderr, returning exit code."""
    for v in violations:
        sys.stderr.write(f"complexity: {v}\n")
    if violations:
        sys.stderr.write("Split the function (guard clauses, extraction, lookup tables) before committing.\n")
        return 1
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """Execute complexity gate check."""
    parser = argparse.ArgumentParser(description="Diff-aware cyclomatic complexity gate.")
    parser.add_argument("--base", metavar="REF", help="Compare working tree against git merge-base REF HEAD.")
    args = parser.parse_args(argv)

    os.chdir(git_cmd("rev-parse", "--show-toplevel").strip())
    base_ref, is_staged = resolve_baseline(args.base)
    records = parse_z_diff(get_raw_diff(base_ref, is_staged))
    candidates = collect_candidates(records, get_exclude_pattern())
    if not candidates:
        return 0
    if shutil.which("lizard") is None:
        sys.stderr.write("complexity: lizard not found (pip install lizard)\n")
        return 2

    limit = get_limit()
    merging = is_staged and is_merging()
    pool = build_moved_out_pool(records, base_ref, is_staged, get_exclude_pattern())
    violations: list[str] = []
    for status, path, old_path in candidates:
        violations.extend(file_violations(status, path, old_path, base_ref, is_staged, limit, pool, merging))
    return report_violations(violations)


if __name__ == "__main__":
    sys.exit(main())
