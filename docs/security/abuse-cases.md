# Abuse cases

Each case describes something an attacker might try and what should
happen. Every one becomes an automated test, or a checked control, in
the sprint listed. Threat IDs (T-xx) refer to `threat-model.md` and
control IDs (ZT-xx) to `requirements.md`.

Tests only ever run against my own local and deployed instances.

| ID | What the attacker tries | Expected result | Threat and controls | Sprint |
|----|------------------------|-----------------|---------------------|--------|
| AC-01 | Guess the admin password by trying many logins in a row | After a small number of failures the endpoint answers 429 and keeps refusing for a period | T-01: ZT-01, ZT-05 | 4 |
| AC-02 | Sign in with a correct password but no TOTP code, or a wrong one | Sign-in is refused and no session is created | T-01: ZT-01 | 4 |
| AC-03 | Reuse a session cookie after logout or after it expired | The request is rejected as unauthenticated | T-01, T-15: ZT-02 | 4 |
| AC-04 | Submit a script tag in the contact form | It is stored and shown as plain text, and the browser runs nothing | T-03: ZT-04, ZT-17 | 3 |
| AC-05 | Put SQL syntax in the form fields | The input is treated as data and the database is unaffected | T-03: ZT-04, ZT-09 | 3 |
| AC-06 | Trick a signed-in admin into submitting a request from another site | A request without a valid CSRF token is rejected | T-15: ZT-03 | 4 |
| AC-07 | Request admin pages without signing in | The response is a redirect to sign in or a 401/403, never the page | T-15: ZT-07 | 4 |
| AC-08 | Flood the contact form with submissions | Excess requests get 429 and the database doesn't fill up | T-13: ZT-05 | 3 |
| AC-09 | Download the public CV and look for private contact details | Only details marked public are in the file | T-10: ZT-11 | 4 |
| AC-10 | Send a malformed request to provoke an error page | A generic message comes back, with no stack trace or file paths | T-08: ZT-14 | 1 |
| AC-11 | Commit a credential to the repository | The pre-commit hook and the CI job both block it | T-07: ZT-15 | 0 |
| AC-12 | Slip a dependency with a known vulnerability into the build | The dependency scan fails the build | T-04: ZT-16 | 1 |