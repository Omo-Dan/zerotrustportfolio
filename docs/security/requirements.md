# Security requirements

These requirements describe what the site and its delivery pipeline must
do to be considered secure. They are grouped by the three zero trust
principles from ADR-0002 and draw on the OWASP Application Security
Verification Standard (ASVS).

Each requirement says how it will be verified and in which sprint it is
delivered. If a requirement can't be checked, it doesn't belong here.

## Verify explicitly

| ID | Requirement | How it's verified | Sprint |
|----|-------------|-------------------|--------|
| ZT-01 | Admin sign-in needs a password, stored as an Argon2id hash, plus a TOTP code. | Automated tests; code review | 4 |
| ZT-02 | Every admin request re-checks the session. Sessions expire after inactivity and are replaced on login. | Automated tests | 4 |
| ZT-03 | Requests that change data carry a CSRF token. Cookies are Secure, HttpOnly and SameSite. | Automated tests | 4 |
| ZT-04 | All input is validated on the server against an allow-list, and all output is escaped. | Automated tests; SAST scan | 3 |
| ZT-05 | The sign-in and contact endpoints are rate limited. | Automated tests | 3 |
| ZT-06 | Deployments are verified: images are signed and checked before release, and cloud access uses short-lived credentials instead of stored keys. | Pipeline configuration; deploy logs | 5-6 |

## Least privilege

| ID | Requirement | How it's verified | Sprint |
|----|-------------|-------------------|--------|
| ZT-07 | Admin routes deny access by default, and each route checks the role it needs. | Automated tests | 4 |
| ZT-08 | Containers run as a non-root user with a read-only filesystem and no extra capabilities. | Container scan; config review | 1 |
| ZT-09 | The application connects to the database with an account that only has the permissions it needs. | Config review; integration test | 3 |
| ZT-10 | CI jobs and cloud roles get only the permissions their task requires. | Pipeline and IaC scans | 1, 5 |
| ZT-11 | The CV export only includes contact details marked as public. | Automated tests | 4 |

## Assume breach

| ID | Requirement | How it's verified | Sprint |
|----|-------------|-------------------|--------|
| ZT-12 | The database is never reachable from the internet. | IaC scan; network config review | 2, 5 |
| ZT-13 | Sign-ins and admin actions are written to an audit log that never contains secrets. | Automated tests | 4 |
| ZT-14 | Errors show a generic message to users. Details go to the logs only. | Automated tests | 1 |
| ZT-15 | Secrets are never committed. Secret scanning runs before each commit and in CI. | Pre-commit hook; CI job | 0 |
| ZT-16 | Dependencies and container images are scanned, and high or critical findings fail the build. | CI scans | 1 |
| ZT-17 | The site is served over TLS only, with HSTS, a strict Content Security Policy and other security headers. | Automated tests; ZAP scan | 1-2 |
| ZT-18 | Backups are encrypted and a restore has been tested. | Restore drill | 6 |
| ZT-19 | The domain registrar account uses MFA and registrar lock, and CAA records limit who can issue certificates. | Manual checklist | 2 |
| ZT-20 | Contact messages are deleted after a fixed retention period. | Automated tests | 3 |



## Code quality

Quality checks run in the same pipeline as the security checks.

| ID | Requirement | How it's verified | Sprint |
|----|-------------|-------------------|--------|
| QA-01 | Code is formatted and linted with ruff. The build fails on violations. | CI job | 1 |
| QA-02 | Type checks pass on every change. | CI job | 1 |
| QA-03 | Automated tests run on every pull request. The build fails if any test fails, and coverage is reported. | CI job | 1 |
| QA-04 | Every security requirement above has at least one test or a documented check. | Review at the end of each sprint | 1-7 |

## Mistakes and account compromise

Most incidents start with an ordinary mistake or a stolen account, so
these controls are automated wherever possible.

| ID | Requirement | How it's verified | Sprint |
|----|-------------|-------------------|--------|
| HE-01 | Production only changes through the pipeline, from the main branch. Nothing is edited by hand on a server. | Repository settings; deploy logs | 0, 2 |
| HE-02 | The main branch requires a pull request and passing checks. The rule applies to me as the owner too, and force pushes are blocked. | Repository settings | 0 |
| HE-03 | Production configuration fails closed. Debug mode is off by default, and the app refuses to start if a required secret or security setting is missing. | Automated tests | 1 |
| HE-04 | Infrastructure is defined as code and scanned for unsafe settings such as open ports and public databases. | IaC scan | 2, 5 |
| HE-05 | Every maintainer account (GitHub, registrar, hosting, cloud) uses MFA. Commits are signed, and access tokens are minimal and short-lived. | Manual checklist | 0, 2 |
| HE-06 | Any release can be rolled back to the previous version quickly. | Rollback drill | 2, 6 |
| HE-07 | The repository never contains personal data or a private email address. Commits use a no-reply address. | Review before the first push; scan in CI | 0 |