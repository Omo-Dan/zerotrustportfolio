# ADR-0003: Image scan policy

Status: accepted
Date: 2026-10-25

## Context
The container image is scanned for known vulnerabilities on every
change. A base operating system image regularly carries high severity
findings for which the distribution has not yet published a fix.
Failing the build on those would keep the pipeline red until someone
else acts, and a check that is always red stops being read. Ignoring
unfixed findings entirely would hide real risk.

## Decision
- The build fails on high or critical findings that have a fix
  available.
- A second scan in the same job prints every high and critical finding,
  fixed or not, and never fails. Unfixed findings stay visible in each
  build log.
- Trivy is installed from a pinned release and checked against a
  published checksum, the same way as gitleaks. It does not run through
  a third-party action.
- The runtime image has no package manager. pip is removed in the same
  layer as the locked install, so the service ships only what it runs.
- Findings are not suppressed with an ignore file. If an exception is
  ever needed, it must record the finding, the reason and a review date.

## Consequences
When a distribution publishes a fix for a finding that was unfixed, the
next build fails until the base image is updated. That is intended.

The scan runs on pull requests, on pushes to main and every Monday.
Advisories appear without any code change, and the weekly run catches
those between changes.

