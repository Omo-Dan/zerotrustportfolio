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