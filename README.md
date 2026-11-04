# boilerbum

[![CI](https://github.com/bumuellp/boilerbum/actions/workflows/ci.yml/badge.svg)](https://github.com/bumuellp/boilerbum/actions/workflows/ci.yml)
[![Renovate](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/bumuellp/.github)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Opinionated starter template for new repositories under `@bumuellp`, featuring centralized Renovate updates, containerized quality gates, single-source reusable CI, and automated template synchronization.

---

## 🚀 Features

- **Single-Source CI**: Invokes the centralized reusable workflow from [`bumuellp/lights-camera-bum-action`](https://github.com/bumuellp/lights-camera-bum-action) pinned by immutable commit SHA.
- **Centralized Renovate**: Extends presets from [`bumuellp/.github:renovate-config`](https://github.com/bumuellp/.github) for vulnerability alerts, cooldown schedules, and grouped updates.
- **Pre-Commit Quality Gates**: Validates formatting, commits, secrets, and security via [`bumuellp/cabumtain-hook`](https://github.com/bumuellp/cabumtain-hook), TruffleHog, and Prettier.
- **Trivy Security Scanning**: Preconfigured [`trivy.yaml`](trivy.yaml) for vulnerability, secret, misconfiguration, and license scans.
- **Automated Template Sync**: Downstream repositories automatically receive weekly PRs whenever `boilerbum` updates via `actions-template-sync`.
- **Environment Consistency**: Normalized line endings (`.gitattributes`) and formatting standards (`.editorconfig`).

---

## 🛠 Usage

### 1. Create a repository from this template

Using the GitHub CLI:

```bash
gh repo create my-new-repo --template bumuellp/boilerbum --public --clone
```

Or click the **Use this template** button on GitHub.

### 2. Set up local pre-commit hooks

```bash
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

### 3. Exclude downstream files from template syncing

Add repository-specific files to [`.templatesyncignore`](.templatesyncignore) to prevent upstream template sync PRs from overwriting local modifications.
