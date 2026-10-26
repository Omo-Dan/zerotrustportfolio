# Changelog

All notable changes are recorded here. The format follows Keep a
Changelog and the project uses semantic versioning.

## [Unreleased]

## [0.1.0] - 2026-10-16

### Added
- Decision records for scope and zero trust principles
- Security requirements, STRIDE threat model and abuse cases, covering
  external attacks and my own mistakes
- Code quality requirements
- Security policy and pull request template
- Pre-commit secret scanning with gitleaks
- CI workflow that scans the full repository history with a pinned,
  checksum-verified gitleaks binary
- Protection on main: pull request and passing secret scan required,
  signed commits only, no force pushes, and no bypass for the owner
- Secret scanning, push protection, Dependabot alerts and security
  updates, and private vulnerability reporting enabled on GitHub
- Signed commits using the GitHub noreply address


## [0.2.0] - 2026-10-25

### Added
- Health endpoint at /healthz
- Security response headers, and API documentation pages hidden
- Generic error responses that never include stack traces or file paths
- Production configuration that fails closed: the app refuses to start unless APP_ENV is an allowed value
- Hash-locked runtime and development requirements, built with pip-compile
- Lint, format and type checks (ruff with security rules, mypy in strict mode) and the test suite, run in a quality job in CI
- Static analysis with Semgrep
- Dependency audit with pip-audit on every change and every Monday
- Container image that runs as an unprivileged user, with a .dockerignore, built in CI with checks for the user ID and the health endpoint
- Image vulnerability scan with Trivy, installed from a pinned, checksum-verified release. The build fails on high or critical findings that have a fix, and all findings are reported (ADR-0003)
- Weekly scheduled run of the container workflow

### Changed
- Main requires the secret scan, quality, Semgrep, dependency audit and container checks, and branches must be up to date before merging
- GitHub Actions are pinned to full commit SHAs
- The runtime image has no package manager: pip is removed after the locked install
- ZT-16 reworded to match the image scan policy

### Security
- certifi updated to 2026.10.19 in the development requirements (PYSEC-2026-4320)