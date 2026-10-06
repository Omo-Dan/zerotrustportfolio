# zerotrustportfolio

My personal portfolio, covering cybersecurity, software development and
cloud. The site itself is simple on purpose. What I'd like you to look at
is how it's built: security requirements and a threat model first, then
code, shipped through an automated pipeline.

## Status
Early development. The design documents are in place. The application,
pipeline and deployments are added step by step, following the roadmap
below. Nothing is live yet.

## How it's designed
The project follows the zero trust principles in NIST SP 800-207: verify
explicitly, use least privilege, assume breach. I only claim a principle
where a control and a test exist.

- Decisions: [docs/adr](docs/adr)
- Security requirements: [docs/security/requirements.md](docs/security/requirements.md)
- Threat model: [docs/security/threat-model.md](docs/security/threat-model.md)
- Abuse cases: [docs/security/abuse-cases.md](docs/security/abuse-cases.md)

## Planned stack
FastAPI and PostgreSQL with server-rendered pages, packaged in Docker,
deployed to Render and AWS (Terraform), built and checked with GitHub
Actions.

## Roadmap
0. Foundations: decisions, requirements, threat model, repository guardrails
1. Secure application skeleton with code, dependency and container scans
2. Automated deployment to Render, plus a dynamic scan of the live site
3. Database, public pages and contact form
4. Admin area with MFA, and CV export
5. AWS deployment with Terraform
6. Image signing, monitoring, backups and a rollback drill
7. A public page showing how the site is built, and the 1.0 release

## How I work
- Conventional Commits, and semantic versioning (see [CHANGELOG.md](CHANGELOG.md))
- Changes go through pull requests with automated checks, even though I
  work alone
- Each security requirement has a test or a documented check

## Security
To report a vulnerability, see [SECURITY.md](SECURITY.md).