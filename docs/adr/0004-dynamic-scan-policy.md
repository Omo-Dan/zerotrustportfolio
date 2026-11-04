# ADR-0004: Dynamic scan policy

Status: accepted
Date: 2026-11-05

## Context
Unit tests check security headers against the application's own list of
headers. They cannot notice a header that was removed from that list, or
one the server fails to send. A dynamic scan reads real responses, so it
checks what a visitor actually receives.

The site has no forms and no sign-in yet, so there is nothing for an
active scan to attack. Scanning production would also add traffic to a
free instance that sleeps when idle.

## Decision
- ZAP's baseline scan, which runs passive checks only, runs on every
  pull request and every push to main. It scans the built container
  image, started on a private network. Production is not scanned.
- The ZAP image is pinned by digest, and the pin is reviewed about once
  a month. A new version arrives as a normal pull request.
- Six rules fail the build: anti-clickjacking (10020),
  X-Content-Type-Options (10021), Strict-Transport-Security (10035),
  Content-Security-Policy (10038), Permissions-Policy (10063) and
  cross-origin isolation (90004). Other findings are reported and do not
  fail the build until they have been reviewed.
- One finding is accepted: storable and cacheable content (10049),
  reported as informational. Every page is public and identical for all
  visitors, so shared caching is acceptable. Any page that handles user
  input or a session must send Cache-Control: no-store before it ships,
  and this rule returns to warning or failure at that point.
- Every rule in the rules file has a written reason on the line above
  it, and a test enforces this. Exceptions follow ADR-0003: the finding,
  the reason and a review point are recorded.
- Cross-origin isolation uses Cross-Origin-Embedder-Policy require-corp,
  Cross-Origin-Opener-Policy same-origin and
  Cross-Origin-Resource-Policy same-origin.

## Consequences
A removed or weakened header fails the build in two independent places,
the unit tests and the scan. This was checked by removing a header on a
temporary commit: both failed, and the change was reverted.

require-corp blocks any cross-origin resource that does not opt in. The
site embeds none, and the content security policy forbids them. If one
is ever added, this policy must be revisited with it.

When the site gains a form or an authenticated area, an active scan
against a test instance is added, with its own decision.

A new ZAP release can add rules that report new findings. They appear as
warnings first, so a ZAP update does not fail the build for reasons
unrelated to a change.