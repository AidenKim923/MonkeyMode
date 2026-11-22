# Security policy

## Supported versions

MonkeyMode is pre-1.0. Security fixes go into the latest release on `main` only.

| Version | Supported |
|---|---|
| 0.1.x (latest) | Yes |
| older | No |

## Reporting a vulnerability

**Do not open a public issue.** Report it privately through GitHub's private vulnerability reporting:

1. Go to the repository's **Security** tab → **Report a vulnerability**, or open <https://github.com/AidenKim923/MonkeyMode/security/advisories/new>.
2. Describe the problem, the affected plugin and file, and how to reproduce it. A minimal proof of concept helps; do not include real secrets or other people's data.

You should get a first reply within 7 days. We will keep you updated while we investigate, agree on a disclosure date with you, and credit you in the advisory unless you prefer not to be named.

## What is in scope

MonkeyMode installs files into game projects and runs local scripts and hooks. Examples of reports we want:

- A hook, setup script or tool that runs commands or writes files outside what it documents
- The guardrail checker or the secrets profile missing a class of secret it claims to catch, or leaking file contents
- A skill or template that tells agents to send project data to an external service without the user asking
- Path traversal, command injection or unsafe file handling in `setup_project.py`, the guardrail checker, the concept/decision page server or the `.ps1` tools

Out of scope: vulnerabilities in Claude Code, Codex, game engines or third-party tools themselves (report those upstream), and guardrail false negatives for ordinary code-quality rules (use the **Guardrail rule** issue form).
