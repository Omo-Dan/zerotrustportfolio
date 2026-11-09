# MFA checklist

Requirements: HE-05 (every maintainer account uses MFA, commits are signed, access tokens are minimal and short-lived), S2-10 (each account is listed and confirmed). Threat: T-20.

This is a manual checklist. A person confirms each account directly in its settings and records the date. The method used for the second factor and the recovery details are deliberately not recorded here.

## Accounts

| Account | MFA | Confirmed | Notes |
| --- | --- | --- | --- |
| GitHub | Enabled | 2026-11-09 | Source code, pipeline and the production environment |
| Render | Enabled | 2026-11-09 | Hosting |
| Registrar | Not applicable yet | | No domain is registered. MFA must be enabled before the first domain is bought (ZT-19). |
| AWS | Not applicable yet | | No account exists. MFA must be enabled on the root user and on every administrator before anything is created. |

The mailbox used to recover these accounts also has MFA enabled. It is not a maintainer account in the sense of HE-05, but it can reset every account above, so it is checked at the same time.

## Commits and tokens

- Commits are signed with an SSH key, and GitHub shows them as Verified.
- The only deploy credential is the Render deploy hook. It is stored as a secret in the `production` GitHub environment, which is restricted to the `main` branch.
- At each review, list the personal access tokens and deploy keys in the GitHub settings and remove any that are not in use.

## Next review

2027-02-09, then every three months. Also review after any phone is replaced or lost, and before any new account is added.