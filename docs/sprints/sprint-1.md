# Sprint 1: Secure application skeleton

Target release: v0.2.0, 26 October 2026

## Goal
A small FastAPI application that runs, is tested, builds into a hardened
container and passes security and quality checks in CI. There are no
features yet. The point is a safe base that every later sprint builds on.

## Backlog
Each item names the requirements it covers (see
`docs/security/requirements.md`) and says when it counts as done.

| ID | Item | Covers | Done when |
|----|------|--------|-----------|
| S1-01 | Confirm each dependency supports Python 3.14 and pin versions | ADR-0001 | Pinned versions install and pass the tests on 3.14 |
| S1-02 | Application skeleton with a health endpoint | | `/healthz` returns 200 |
| S1-03 | Security headers on every response | ZT-17 | A test checks each header |
| S1-04 | Generic error responses | ZT-14, AC-10 | A malformed request returns a plain message with no stack trace or paths |
| S1-05 | Configuration that fails closed | HE-03, AC-14 | Debug is off by default, and the app refuses to start in production without its required settings |
| S1-06 | Lint, type check and tests in CI | QA-01, QA-02, QA-03 | CI fails when any of them fails, and coverage is reported |
| S1-07 | Static analysis (SAST) | ZT-04 | The scan job fails on a high-severity finding |
| S1-08 | Dependency scan | ZT-16, AC-12 | The scan job fails on a known vulnerability |
| S1-09 | Container image that runs as a non-root user | ZT-08 | The image builds in CI and the container runs as a non-root user |
| S1-10 | Container image scan | ZT-16 | The scan job fails on a high or critical finding that has a fix available |

| S1-12 | GitHub Actions pinned to commit SHAs | ZT-10 | Every `uses:` line references a full commit SHA |

## Order of work
Tests come first. For each item I write the check that proves it (a test
or a failing CI job), see it fail, then write the code that makes it pass.

## Definition of done
- The requirements above are met and traced to a test or a CI check.
- CI is green and every commit is signed.
- The changelog is updated and the release is tagged.

## Not in this sprint
Deployment, the database, the public pages and the admin area. Dependabot
version updates (formerly S1-11) are planned for sprint 2.