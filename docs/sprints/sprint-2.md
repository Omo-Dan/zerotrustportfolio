# Sprint 2: Live site

Target release: v0.3.0

## Goal
The site is live on Render, deployed only by the pipeline after the
checks pass, and it has its first public pages. The live site is
scanned, and the delivery process is proven to be recoverable.

## Backlog
Each item names the requirements it covers (see
`docs/security/requirements.md`) and says when it counts as done.

| ID | Item | Covers | Done when |
|----|------|--------|-----------|
| S2-01 | Deploy to Render from the pipeline | HE-01 | Only the deploy job changes production, after the checks pass on main, and auto-deploy is off |
| S2-02 | Landing page | ZT-17 | The page is served with the security headers and has tests |
| S2-03 | Skills page, including certifications | ZT-17 | The page is served with the security headers and has tests |
| S2-04 | About page | ZT-17 | The page is served with the security headers and has tests |
| S2-05 | Projects page | ZT-17 | The page is served with the security headers and has tests |
| S2-06 | ZAP baseline scan of the live site | ZT-17 | The scan runs against the deployed site and its report is kept |
| S2-07 | Dependabot for Python packages, GitHub Actions and Docker | ZT-16 | Update pull requests appear and pass through the same checks |
| S2-08 | Replace httpx with httpx2 in the tests | QA-03 | The deprecation warning is gone and the tests pass |
| S2-09 | Rollback drill | HE-06, AC-15 | A previous release is restored and the health check answers within minutes |
| S2-10 | Multi-factor authentication on every maintainer account | HE-05 | Each account is listed and confirmed |

## Order of work
Tests come first. For each item I write the check that proves it (a test
or a failing CI job), see it fail, then write the code that makes it pass.

## Definition of done
- The requirements above are met and traced to a test or a CI check.
- CI is green and every commit is signed.
- The changelog is updated and the release is tagged.

## Not in this sprint
The database, the contact form, the admin area and CV export.