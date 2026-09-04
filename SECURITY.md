# Security Policy

## Scope

JobHunter is a local-first personal career-intelligence application, not a hosted multi-user service.

The current security boundary includes:

- a browser application that binds to loopback by default;
- local SQLite/evidence/runtime state that is intentionally excluded from Git;
- optional local LM Studio inference;
- bounded public Jobinja acquisition;
- optional external translation only when explicitly configured;
- a deterministic repository-safe public corpus that excludes machine-local/private state.

Security reports are especially relevant when they involve unintended network exposure, source-policy bypass, unsafe handling/rendering of acquired content, CSRF/security-header failures, secret/private-data disclosure, path traversal, public-corpus leakage, or dependency/supply-chain vulnerabilities affecting JobHunter.

## Supported code

Until JobHunter has a stable tagged release, security fixes target the current `main` branch. Historical/versioned semantic implementations are retained for compatibility and reproducibility but are not all independent supported product versions.

## Reporting a vulnerability

Do not include API keys, access tokens, private career data, local database contents, or other secrets in a public issue.

For a report that is safe to discuss publicly, open a GitHub issue with the smallest useful reproduction and impact description.

For a report that requires sensitive details, prefer GitHub's private vulnerability-reporting/security-advisory path when it is available for the repository. If that path is unavailable, contact the repository owner through the GitHub profile first and disclose only enough non-secret information to establish a private reporting channel.

Please include when possible:

- affected commit/version;
- affected interface or command;
- reproduction conditions;
- observed versus expected behavior;
- security impact;
- whether the issue requires LM Studio, live Jobinja access, or non-default network binding.

## Secrets and local state

Do not commit:

- `.env` files or credentials;
- LM Studio/API tokens;
- Google Cloud translation keys;
- SQLite/WAL/SHM runtime databases;
- raw local evidence/logs;
- machine-specific private configuration;
- future personal evidence, applications, notes, or profile data.

Use ignored `config/local.*` files or process environment variables for machine-local configuration. The tracked `jobhunter.toml` is a maintainer/runtime reference and must not contain secrets.

## Public corpus boundary

`corpus/` is intentionally public. Its exporter allowlists current public job-domain artifacts and excludes SQLite files, raw model protocol/request bodies, prompts, secrets, logs, machine-local paths, pending/rejected semantic candidates, and future private/personal evidence.

A suspected public-corpus leak is treated as a security/privacy defect, not a documentation issue.

## Network exposure

The browser binds to loopback by default. Binding outside loopback requires explicit `--allow-network` intent and should be used only on a trusted network. JobHunter is not currently designed or claimed as an internet-facing production service.
