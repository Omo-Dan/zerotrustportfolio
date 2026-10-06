# ADR-0002: Project name and zero trust principles

Status: accepted
Date: 2026-10-02

## Context
The project needed a clear security theme to guide design choices.

## Decision
The project is called zerotrustportfolio. It follows the zero trust
principles in NIST SP 800-207: verify explicitly, use least privilege,
and assume breach.

They apply to the admin area, the CI/CD pipeline and the cloud
environment. Public pages stay anonymous and read-only.

## Consequences
Each design choice should trace back to one of the principles. Zero
trust is only claimed where a control and a test exist.
