# Changelog

All notable changes are recorded here. The format follows Keep a
Changelog and the project uses semantic versioning.

## [Unreleased]

## [0.3.0] - 2026-11-17

### Added
- Live site on Render. Only the deploy job changes production, after the checks pass on main, and Render's own auto-deploy is off
- Version endpoint at /version, and a deploy job that waits until the live site reports the commit it just deployed
- Public pages: landing, About, Projects, Skills and Certifications, with a shared layout and navigation
- Dark-first design with colour tokens, a skip link, visible focus and reduced-motion support
- Cross-origin isolation headers (COOP, COEP, CORP)
- Dynamic scan with the OWASP ZAP baseline against the built container on a private network, pinned by digest, with the header rules set to fail the build (ADR-0004)
- Dependabot for Python packages, GitHub Actions and Docker, weekly, with a seven-day cooldown. Python image upgrades are ignored on purpose
- Rollback runbook with two paths, a standard signed revert and a faster dashboard rollback, both timed in a drill
- Multi-factor authentication checklist for every maintainer account

### Changed
- Main requires six checks, including the ZAP baseline
- The base image is pinned by digest
- httpx replaced by httpx2 in the tests, and the Starlette warning now fails the test run

### Security
- Base image digest updated for a fixable apt finding, and a marked temporary zlib upgrade until the base image ships the fix
- opentelemetry-api updated to 1.45.2

## [0.2.0] - 2026-10-26

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