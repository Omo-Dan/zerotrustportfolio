# ADR-0001: Project scope and key decisions

Status: accepted
Date: 2026-10-02

## Context
zerotrustportfolio is my personal portfolio site, covering cybersecurity,
software development and cloud. Security requirements come first and
everything ships through an automated pipeline, so the repository shows
how the site is built as well as what it contains.

## Decisions
1. The repository is public. The way the site is built is part of what
   it demonstrates.
2. No personal data lives in the repo. Real content is entered through
   the admin area, which keeps code and content separate.
3. Pages are rendered on the server (FastAPI and Jinja2) with plain CSS,
   no inline scripts and no third-party CDNs. A strict Content Security
   Policy only works if those are absent.
4. One admin account and no public signup, which keeps the number of
   entry points small.
5. Contact messages are stored in the database. There is no email
   sending in v1, so there are no mail credentials to protect.
6. A privacy notice and a retention period apply to contact messages, so
   personal data is only kept as long as it is needed.
7. Logs are structured JSON with request IDs, so events can be traced.
8. Python 3.14 with pinned dependencies, for reproducible builds.
9. Every change goes through a pull request, even as a solo developer,
   so it passes the same automated checks.
10. Domain: danielojiambo.me
11. A budget alert is set before any AWS resource is created.
12. Scan results are kept as CI artifacts.

## Scope of v1.0
In: public pages, contact form, admin area, CV export, deployment to
Render and AWS.
Out: blog, comments, multiple languages, public accounts.

## Consequences
A simple front end limits interactivity but keeps the attack surface
small and the pipeline easy to reason about.
