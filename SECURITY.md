# Security Policy

## Reporting a Vulnerability

If you find a security vulnerability in Cookiecutter PyPackage, please report it through [GitHub's private vulnerability reporting](https://github.com/audreyfeldroy/cookiecutter-pypackage/security/advisories/new). This keeps the details private while we work on a fix.

Please include:

- What you found and how to reproduce it
- Which version you're using
- Any relevant logs or output (redact secrets)

## What's in Scope

This project has two layers, and vulnerabilities can exist in either:

**The template itself** (this repo):
- Hooks that execute during project generation (`hooks/`)
- Dependencies pulled in by the template tooling
- The CLI (`cookiecutter-pypackage` command)

**Generated projects** (what you get after baking):
- Default dependency versions that ship with known vulnerabilities
- CI workflow configurations that could leak secrets or be exploited
- Insecure default settings in generated config files

If you're unsure which layer a vulnerability belongs to, report it here.

## Security Measures

Generated projects ship with security hardening out of the box:

- **CodeQL** scans code for injection, SSRF, path traversal, and other dataflow vulnerabilities using the `security-extended` query suite
- **Zizmor** audits GitHub Actions workflows for excessive permissions, unpinned actions, credential exposure, and cache poisoning risks
- **Dependabot** keeps GitHub Actions pinned by SHA and opens PRs for updates, with a 7-day cooldown to avoid adopting compromised releases immediately
- **All actions pinned by SHA** with version comments, not floating tags
- **Minimal workflow permissions** (`permissions: {}` at the top level, scoped per job)
- **`persist-credentials: false`** on checkout steps to prevent token leakage

## Response Times

This is a volunteer-maintained open source project. Security reports are taken seriously, but there are no guaranteed response times.

**Enterprise support** is available, with priority response SLAs. Contact support@feldroy.com for details.

## Supported Versions

Security fixes are applied to the latest release on the `main` branch. There is no backport policy for older versions.
