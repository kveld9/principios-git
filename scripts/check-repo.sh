#!/usr/bin/env bash
# ==============================================================================
# Repository Standards Audit Script
#
# Inspects a target directory for compliance with the GitHub Standards Kit.
# Verifies file presence, non-zero file sizes, and core structural health.
#
# Usage:
#   ./scripts/check-repo.sh [target_directory]
#   If target_directory is omitted, checks the current directory.
#
# Exit codes:
#   0 - All standard and required files exist.
#   1 - One or more required files are missing or empty.
# ==============================================================================

set -euo pipefail

TARGET_DIR="${1:-.}"

if [[ ! -d "${TARGET_DIR}" ]]; then
  echo "Error: Target directory '${TARGET_DIR}' does not exist." >&2
  exit 1
fi

TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Color formatting if connected to a terminal
if [[ -t 1 ]]; then
  GREEN='\033[0;32m'
  RED='\033[0;31m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  BOLD='\033[1m'
  RESET='\033[0m'
else
  GREEN=''
  RED=''
  YELLOW=''
  BLUE=''
  BOLD=''
  RESET=''
fi

echo -e "${BOLD}${BLUE}==> Auditing repository standards at: ${TARGET_DIR}${RESET}\n"

check_file() {
  local rel_path="$1"
  local is_critical="${2:-true}"
  local full_path="${TARGET_DIR}/${rel_path}"

  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

  if [[ -f "${full_path}" ]]; then
    if [[ -s "${full_path}" ]]; then
      echo -e "  [${GREEN}OK${RESET}] ${rel_path}"
      PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
      echo -e "  [${YELLOW}EMPTY${RESET}] ${rel_path} (file is 0 bytes)"
      if [[ "${is_critical}" == "true" ]]; then
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
      else
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
      fi
    fi
  else
    if [[ "${is_critical}" == "true" ]]; then
      echo -e "  [${RED}MISSING${RESET}] ${rel_path} (REQUIRED)"
      FAILED_CHECKS=$((FAILED_CHECKS + 1))
    else
      echo -e "  [${YELLOW}OPTIONAL${RESET}] ${rel_path} (recommended)"
    fi
  fi
}

echo -e "${BOLD}1. Root Metadata & Licensing${RESET}"
check_file "README.md" true
check_file "LICENSE" true
check_file "CONTRIBUTING.md" true
check_file "CODE_OF_CONDUCT.md" true
check_file "SECURITY.md" true
check_file "CHECKLIST.md" true

echo -e "\n${BOLD}2. Git & Environment Configuration${RESET}"
check_file ".gitignore" true
check_file ".gitattributes" true
check_file ".editorconfig" true

echo -e "\n${BOLD}3. GitHub Automation & Templates (.github/)${RESET}"
check_file ".github/workflows/ci.yml" true
check_file ".github/dependabot.yml" true
check_file ".github/ISSUE_TEMPLATE/bug_report.md" true
check_file ".github/ISSUE_TEMPLATE/feature_request.md" true
check_file ".github/PULL_REQUEST_TEMPLATE.md" true
check_file ".github/CODEOWNERS.example" false
check_file ".github/settings.example.yml" false

echo -e "\n${BOLD}4. Documentation Architecture (docs/)${RESET}"
check_file "docs/01-principios.md" true
check_file "docs/02-estructura-repo.md" true
check_file "docs/03-branching.md" true
check_file "docs/04-commits.md" true
check_file "docs/05-pull-requests.md" true
check_file "docs/06-releases.md" true
check_file "docs/07-ci.md" true
check_file "docs/08-seguridad.md" true
check_file "docs/09-licencias.md" true
check_file "docs/10-adopcion.md" true
check_file "docs/11-estilo.md" true
check_file "docs/12-modularizacion.md" true

echo -e "\n${BOLD}5. Maintenance & Setup Automation (scripts/)${RESET}"
check_file "scripts/check-repo.sh" true
check_file "scripts/new-repo.sh" true

echo -e "\n--------------------------------------------------"
echo -e "Audit Summary: ${TOTAL_CHECKS} checked | ${GREEN}${PASSED_CHECKS} passed${RESET} | ${RED}${FAILED_CHECKS} failed${RESET}"

if [[ ${FAILED_CHECKS} -gt 0 ]]; then
  echo -e "${RED}${BOLD}Result: FAILED - Required standard files are missing or empty.${RESET}\n"
  exit 1
else
  echo -e "${GREEN}${BOLD}Result: PASSED - Repository satisfies all structural standards.${RESET}\n"
  exit 0
fi
