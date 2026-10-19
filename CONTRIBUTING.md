# Contributing to This Project

Thank you for your interest in contributing! We welcome contributions that improve code quality, documentation, performance, and user experience while maintaining rigorous engineering standards.

Please review this document and our [Code of Conduct](CODE_OF_CONDUCT.md) before submitting contributions.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Workflow](#development-workflow)
  - [1. Branch Naming](#1-branch-naming)
  - [2. Commit Conventions](#2-commit-conventions)
  - [3. Code Style & Standards](#3-code-style--standards)
- [Pull Request Checklist](#pull-request-checklist)
- [Further Reading](#further-reading)

---

## Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to `security@example.com` or the designated project contact.

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check existing issues to ensure the problem has not already been reported.

When opening a bug report via our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md), include:
- A clear, descriptive title.
- Clear reproduction steps.
- Expected behavior vs. actual behavior.
- Relevant logs, error outputs, and environment details (OS, toolchain versions).
- A minimal reproducible example whenever possible.

### Suggesting Enhancements

Feature requests and architectural changes should be submitted using the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md). Provide:
- The problem or limitation you are trying to solve.
- The proposed solution and rationale.
- Any alternative approaches considered.

### Submitting Pull Requests

1. **Keep Changes Focused**: Each pull request should address a single concern, fix, or feature. Avoid bundling unrelated formatting, refactoring, or unrelated changes into one PR.
2. **Open an Issue First**: For non-trivial features or refactorings, discuss the proposal in an issue before writing code to align on direction.
3. **Draft PRs**: Open a draft PR early if you want feedback on architecture or work-in-progress.

---

## Development Workflow

### 1. Branch Naming

Create a dedicated branch from `main`:

```bash
git checkout -b <type>/<short-description>
```

Branch types:
- `feat/`: New user-facing feature or enhancement
- `fix/`: Bug fix
- `refactor/`: Code reorganization without behavioral change
- `docs/`: Documentation updates
- `test/`: Adding or modifying tests
- `chore/`: Build tasks, dependencies, tooling updates

*Examples:*
- `feat/jwt-authentication`
- `fix/connection-timeout`
- `docs/readme-quickstart`

### 2. Commit Conventions

We follow the **Conventional Commits** specification (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`, etc.):

```text
<type>(<scope>): <short summary in imperative mood>

[optional body explaining motivation and trade-offs]

[optional footer(s), e.g. Fixes #123]
```

- Write commit messages strictly in English.
- Use imperative present tense ("add feature" not "added feature").
- Keep commits atomic: one logical change per commit.
- Do not use emojis in commit messages (see [`docs/11-estilo.md`](docs/11-estilo.md)).
- For in-depth rules and examples, see [`docs/04-commits.md`](docs/04-commits.md).

### 3. Code Style & Standards

- **Emoji Prohibition**: Emojis are strictly prohibited in code, scripts, configuration files, CLI logs, CI workflows, filenames, and commit messages. They are permitted exclusively in human-facing documentation (`README.md`, `docs/`) and release notes. See [`docs/11-estilo.md`](docs/11-estilo.md).
- **Formatting**: Ensure your editor respects [`.editorconfig`](.editorconfig) settings (UTF-8, LF line endings, 2 or 4 spaces indentation as specified).
- **Line Endings**: Always commit with LF line endings as configured in [`.gitattributes`](.gitattributes).
- **Linters & Tests**: Run repository linters and test suites before submitting changes.
- **Dependencies & Simplicity**: Do not introduce unnecessary external dependencies. Prefer minimal, standard-library-driven solutions where feasible.
- **Clean Code Standards**: Write small, single-responsibility functions with low cyclomatic complexity. Avoid magic numbers and strings by defining named constants. Never suppress errors silently (e.g., empty catch blocks or `|| true`); follow fail-loud error handling. Keep code clean of commented-out dead code, and apply DRY pragmatically without premature abstraction. See [`docs/11-estilo.md`](docs/11-estilo.md).
- **Modular Architecture**: Enforce high internal cohesion, explicit contracts, and unidirectional dependencies without cycles. Organize code by feature or domain rather than generic technical file types. See [`docs/12-modularizacion.md`](docs/12-modularizacion.md).

---

## Pull Request Checklist

Before marking your PR as ready for review, verify:

- [ ] The PR addresses a single problem or feature (atomic scope).
- [ ] Commits follow Conventional Commits format without emojis.
- [ ] No emojis in code, scripts, configuration files, or CLI logs ([`docs/11-estilo.md`](docs/11-estilo.md)).
- [ ] Code adheres to clean code, error handling, and modularity standards ([`docs/11-estilo.md`](docs/11-estilo.md), [`docs/12-modularizacion.md`](docs/12-modularizacion.md)).
- [ ] All tests pass locally and no regressions are introduced.
- [ ] Documentation was updated if behavior, flags, configuration, or APIs changed.
- [ ] No temporary files, debug statements, or secrets were committed.
- [ ] PR description details the changes, rationale, and links relevant issues (`Fixes #<issue>`).

---

## Further Reading

Detailed architectural and procedural standards can be found in the [`docs/`](docs/) directory:
- [Git Principles & Philosophy](docs/01-principios.md)
- [Repository Structure Standard](docs/02-estructura-repo.md)
- [Branching Strategy](docs/03-branching.md)
- [Commit Discipline](docs/04-commits.md)
- [Pull Request & Code Review Guide](docs/05-pull-requests.md)
- [Releases & Semantic Versioning](docs/06-releases.md)
- [Continuous Integration Standards](docs/07-ci.md)
- [Security Practices](docs/08-seguridad.md)
- [License Guide](docs/09-licencias.md)
- [Kit Adoption Guide](docs/10-adopcion.md)
- [Code Style & Professional Standards](docs/11-estilo.md)
- [Modularization & Component Architecture](docs/12-modularizacion.md)
