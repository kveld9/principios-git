#!/usr/bin/env bash
# ==============================================================================
# Repository Scaffolding & Kit Adoption Tool
#
# Bootstraps an empty or existing repository with the complete GitHub
# Standards Kit (.github/, docs/, config, licenses, and verification scripts).
#
# Usage:
#   ./scripts/new-repo.sh [options] <target_directory>
#
# Options:
#   -f, --force         Overwrite existing files in target directory.
#   -o, --owner <name>  Owner or Organization name for LICENSE / CODEOWNERS.
#   -y, --year <year>   Copyright year (defaults to current year).
#   -e, --email <email> Security & conduct contact email (defaults to security@example.com).
#   -h, --help          Show this help message.
#
# Example:
#   ./scripts/new-repo.sh --owner "MyOrg" --email "team@myorg.com" /path/to/new-repo
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

FORCE=false
OWNER="[OWNER]"
YEAR="$(date +%Y)"
EMAIL="security@example.com"
TARGET_DIR=""

show_help() {
  cat << EOF
Repository Scaffolding & Standards Kit Installer

Usage:
  $(basename "$0") [options] <target_directory>

Arguments:
  target_directory   Directory where the standards kit will be initialized.

Options:
  -f, --force        Overwrite existing files.
  -o, --owner <str>  Owner / Copyright holder name (defaults to "[OWNER]").
  -y, --year <num>   Copyright year (defaults to current year: ${YEAR}).
  -e, --email <str>  Contact email for security and conduct reports.
  -h, --help         Display this help message and exit.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -f|--force)
      FORCE=true
      shift
      ;;
    -o|--owner)
      if [[ $# -lt 2 ]]; then
        echo "Error: option '$1' requires a value." >&2
        show_help
        exit 1
      fi
      OWNER="$2"
      shift 2
      ;;
    -y|--year)
      if [[ $# -lt 2 ]]; then
        echo "Error: option '$1' requires a value." >&2
        show_help
        exit 1
      fi
      YEAR="$2"
      shift 2
      ;;
    -e|--email)
      if [[ $# -lt 2 ]]; then
        echo "Error: option '$1' requires a value." >&2
        show_help
        exit 1
      fi
      EMAIL="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    -*)
      echo "Error: Unknown option '$1'" >&2
      show_help
      exit 1
      ;;
    *)
      if [[ -z "${TARGET_DIR}" ]]; then
        TARGET_DIR="$1"
      else
        echo "Error: Unexpected argument '$1'" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "${TARGET_DIR}" ]]; then
  echo "Error: Missing target directory." >&2
  show_help
  exit 1
fi

mkdir -p "${TARGET_DIR}"
TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"

echo "==> Initializing GitHub Standards Kit into: ${TARGET_DIR}"
echo "    Owner: ${OWNER}"
echo "    Year:  ${YEAR}"
echo "    Email: ${EMAIL}"
echo "    Force: ${FORCE}"

escape_sed() {
  printf '%s' "$1" | sed -e 's|\\|\\\\|g' -e 's|/|\\/|g' -e 's|&|\\&|g'
}

OWNER="$(escape_sed "${OWNER}")"
YEAR="$(escape_sed "${YEAR}")"
EMAIL="$(escape_sed "${EMAIL}")"

copy_file() {
  local src="$1"
  local dest="$2"

  if [[ -f "${dest}" ]] && [[ "${FORCE}" != "true" ]]; then
    echo "  [SKIP] ${dest#${TARGET_DIR}/} (already exists, use --force to overwrite)"
    return 0
  fi

  mkdir -p "$(dirname "${dest}")"
  cp "${src}" "${dest}"

  # Substitute template placeholders if copying into target
  if [[ -f "${dest}" ]]; then
    sed -i "s/\[YEAR\]/${YEAR}/g" "${dest}" 2>/dev/null
    sed -i "s/\[OWNER\]/${OWNER}/g" "${dest}" 2>/dev/null
    sed -i "s/security@example.com/${EMAIL}/g" "${dest}" 2>/dev/null
    sed -i "s/@kveld9/@${OWNER#@}/g" "${dest}" 2>/dev/null
  fi

  echo "  [CREATE] ${dest#${TARGET_DIR}/}"
}

# 1. Root Configuration & Community Health Files
copy_file "${KIT_ROOT}/.editorconfig" "${TARGET_DIR}/.editorconfig"
copy_file "${KIT_ROOT}/.gitattributes" "${TARGET_DIR}/.gitattributes"
copy_file "${KIT_ROOT}/.gitignore" "${TARGET_DIR}/.gitignore"
copy_file "${KIT_ROOT}/.markdownlint.yaml" "${TARGET_DIR}/.markdownlint.yaml"
copy_file "${KIT_ROOT}/LICENSE" "${TARGET_DIR}/LICENSE"
copy_file "${KIT_ROOT}/CODE_OF_CONDUCT.md" "${TARGET_DIR}/CODE_OF_CONDUCT.md"
copy_file "${KIT_ROOT}/SECURITY.md" "${TARGET_DIR}/SECURITY.md"
copy_file "${KIT_ROOT}/CONTRIBUTING.md" "${TARGET_DIR}/CONTRIBUTING.md"
copy_file "${KIT_ROOT}/CHECKLIST.md" "${TARGET_DIR}/CHECKLIST.md"
copy_file "${KIT_ROOT}/README.md" "${TARGET_DIR}/README.md"
copy_file "${KIT_ROOT}/.releaserc.js.example" "${TARGET_DIR}/.releaserc.js.example"

# 2. GitHub Automation & Templates (.github/)
mkdir -p "${TARGET_DIR}/.github/workflows"
mkdir -p "${TARGET_DIR}/.github/ISSUE_TEMPLATE"
copy_file "${KIT_ROOT}/.github/workflows/ci.yml" "${TARGET_DIR}/.github/workflows/ci.yml"
copy_file "${KIT_ROOT}/.github/workflows/release.yml.example" "${TARGET_DIR}/.github/workflows/release.yml.example"
copy_file "${KIT_ROOT}/.github/workflows/gitleaks.yml" "${TARGET_DIR}/.github/workflows/gitleaks.yml"
copy_file "${KIT_ROOT}/.github/workflows/codeql.yml.example" "${TARGET_DIR}/.github/workflows/codeql.yml.example"
copy_file "${KIT_ROOT}/.github/dependabot.yml" "${TARGET_DIR}/.github/dependabot.yml"
copy_file "${KIT_ROOT}/.github/ISSUE_TEMPLATE/bug_report.md" "${TARGET_DIR}/.github/ISSUE_TEMPLATE/bug_report.md"
copy_file "${KIT_ROOT}/.github/ISSUE_TEMPLATE/feature_request.md" "${TARGET_DIR}/.github/ISSUE_TEMPLATE/feature_request.md"
copy_file "${KIT_ROOT}/.github/PULL_REQUEST_TEMPLATE.md" "${TARGET_DIR}/.github/PULL_REQUEST_TEMPLATE.md"
copy_file "${KIT_ROOT}/.github/CODEOWNERS" "${TARGET_DIR}/.github/CODEOWNERS"
copy_file "${KIT_ROOT}/.github/CODEOWNERS.example" "${TARGET_DIR}/.github/CODEOWNERS.example"
copy_file "${KIT_ROOT}/.github/settings.example.yml" "${TARGET_DIR}/.github/settings.example.yml"

# 3. Documentation Guide (docs/)
mkdir -p "${TARGET_DIR}/docs"
for doc_file in "${KIT_ROOT}"/docs/*.md; do
  if [[ -f "${doc_file}" ]]; then
    copy_file "${doc_file}" "${TARGET_DIR}/docs/$(basename "${doc_file}")"
  fi
done

# 4. Verification & Scaffolding Scripts (scripts/)
mkdir -p "${TARGET_DIR}/scripts"
copy_file "${KIT_ROOT}/scripts/check-repo.sh" "${TARGET_DIR}/scripts/check-repo.sh"
copy_file "${KIT_ROOT}/scripts/new-repo.sh" "${TARGET_DIR}/scripts/new-repo.sh"
chmod +x "${TARGET_DIR}/scripts/"*.sh 2>/dev/null || true

echo -e "\n==> GitHub Standards Kit setup completed successfully."
echo "    Run '${TARGET_DIR}/scripts/check-repo.sh' to audit compliance."
