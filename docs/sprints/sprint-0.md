# Sprint 0: Foundations

Release: v0.1.0, 16 October 2026

## Goal
Put the security groundwork in place before any application code:
decisions, requirements, a threat model and guardrails for the repository.

## Delivered
- Decision records (ADR-0001, ADR-0002)
-- 31 requirements: 20 zero trust controls, 4 code quality checks and 7
  controls for mistakes and account compromise
  plus 7 controls for mistakes and account compromise
- STRIDE threat model with 21 threats mapped to controls
- 15 abuse cases, each phrased so it can become a test
- Security policy, pull request template, README and changelog
- Secret scanning in three places: pre-commit, CI over the full
  history, and GitHub push protection
- Protected main branch, signed commits and a private commit identity

## Evidence
- The pre-commit hook blocked a commit containing a fake token (AC-11).
- CI scanned all 18 commits and found no leaks.
- A direct push to main was rejected by GitHub, with the rule applying
  to the owner (AC-13, HE-02).
- Every commit shows as Verified on GitHub.
- History was rewritten before the first push so no personal email
  address is public (HE-07).

## Retrospective
What went well: the requirements, threat model and abuse cases now give
every later sprint something concrete to test against.

What I'd change: the first CI run failed because the scan action only
examined the commits in each push and could not handle the root commit.
I replaced it with a pinned, checksum-verified binary that scans the
whole history. I would also set up commit identity and signing before
the first commit, which would have avoided rewriting history.

## Next: Sprint 1
A secure application skeleton with a health check, security headers and
tests, plus static analysis, dependency, container and quality checks
in CI.