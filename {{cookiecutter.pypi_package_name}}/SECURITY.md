# Security Policy

## Reporting a Vulnerability

If you find a security vulnerability in {{ cookiecutter.project_name }}, please report it through [GitHub's private vulnerability reporting](https://github.com/{{ cookiecutter.__gh_slug }}/security/advisories/new). This keeps the details private while we work on a fix.

Please include:

- What you found and how to reproduce it
- Which version you're using
- Any relevant logs or output (redact secrets)

## Security Measures

This project ships with security hardening out of the box:

- **CodeQL** scans code for injection, SSRF, path traversal, and other dataflow vulnerabilities using the `security-extended` query suite
- **Zizmor** audits GitHub Actions workflows for excessive permissions, unpinned actions, credential exposure, and cache poisoning risks
- **Dependabot** keeps GitHub Actions pinned by SHA and opens PRs for updates, with a 7-day cooldown to avoid adopting compromised releases immediately
- **All actions pinned by SHA** with version comments, not floating tags
- **Minimal workflow permissions** (`permissions: {}` at the top level, scoped per job)
- **`persist-credentials: false`** on checkout steps to prevent token leakage

## Response Times

This is a volunteer-maintained open source project. Security reports are taken seriously, but there are no guaranteed response times.

**Enterprise support** is available, with priority response SLAs. Contact {{ cookiecutter.email }} for details.

## Supported Versions

Security fixes are applied to the latest release on the `main` branch. There is no backport policy for older versions.
