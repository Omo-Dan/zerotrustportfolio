# Sprint 3: Content in a database

Target release: v0.4.0

## Goal
The content of the public pages lives in a database instead of in
template files, only items marked as published ever reach a visitor,
and the first piece of the admin area, sign-in with a second factor,
is in place. The rollback drill from Sprint 2 is recorded.

## Backlog
Each item names the requirements it covers (see
`docs/security/requirements.md`) and says when it counts as done.

| ID | Item | Covers | Done when |
|----|------|--------|-----------|
| S3-01 | Record the rollback drill | HE-06, AC-15 | The runbook has a dated drill log with measured times for both paths, and says what the drill does not prove |
| S3-02 | ADR-0005: content and CV data model | ZT-11, T-10 | The decision record covers the engine, the data model, the hidden, learning and published statuses, the role tags, and the separate show-on-site and include-in-CV flags |
| S3-03 | Database and connection | ZT-12 | The app reaches a database with credentials that are never in the repository, and the app user has only the access it needs |
| S3-04 | Content model | ZT-11 | Skills, certifications and projects are stored in tables, and a test proves that items that are not published never appear on a public page |
| S3-05 | Skills page read from the database | ZT-17 | The page looks the same to a visitor, keeps its security headers, and the existing page tests still pass |
| S3-06 | Abuse cases and requirements for admin sign-in | ZT-04 | The threat model and abuse cases for the admin area are written and reviewed before any sign-in code |
| S3-07 | Admin sign-in with a second factor | ZT-04 | Only a signed-in admin with MFA reaches the admin area, and tests cover failed and missing sign-in |

## Order of work
Tests come first. For each item I write the check that proves it (a test
or a failing CI job), see it fail, then write the code that makes it pass.
Decisions that change the design are written down as ADRs before code.

## Definition of done
- The requirements above are met and traced to a test or a CI check.
- CI is green and every commit is signed.
- The changelog is updated and the release is tagged.

## Not in this sprint
The contact form, CV export, the admin pages for editing content, and
the AWS deployment.