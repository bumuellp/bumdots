# bumdots

[![CI](https://github.com/bumuellp/bumdots/actions/workflows/ci.yml/badge.svg)](https://github.com/bumuellp/bumdots/actions/workflows/ci.yml)
[![Renovate](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/bumuellp/.github)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Personal public dotfiles library for `@bumuellp`, built on a bare Git repository architecture with a seamless **Public (Base) + Private (Overlay)** split.

---

## 🏗 Architecture Overview

The dotfiles repository uses a **bare Git repository** located at `$HOME/repos/bumdots` with its worktree set directly to `$HOME`. Untracked files in the home directory are ignored by default.

Configurations are decoupled into two layers to ensure private server IPs, work credentials, and local environment tokens are never committed publicly:

| Layer       | Repository            | Visibility  | Tracked Files                                                                                                                                     |
| :---------- | :-------------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Base**    | `bumdots`             | **Public**  | Shell configs (`.bashrc`, `.profile`), tool settings (`.yamllint`, gh/glab configs), generic SSH rules, and public Git profiles.                  |
| **Overlay** | `private-dots` (opt.) | **Private** | Infrastructure IPs (`~/.ssh/config.local`), company/university identities (`~/.gitconfig.local`), and local workspace settings (`settings.json`). |

---

## 🚀 Initial Setup & Alias Configuration

Add the following alias and safeguarded include hook to your `~/.bashrc`:

```bash
# Dotfiles repository alias
alias dotfiles='/usr/bin/git --git-dir=$HOME/repos/bumdots/ --work-tree=$HOME'

# Safeguarded local/private shell additions
if [ -f "$HOME/.bashrc.local" ]; then
  . "$HOME/.bashrc.local"
fi
```

### Essential Configuration

Ensure untracked files in `$HOME` are hidden from `git status`:

```bash
dotfiles config --local status.showUntrackedFiles no
```

### Installing Pre-Commit Quality Gates

Install pre-commit hooks for the bare repository:

```bash
GIT_DIR=$HOME/repos/bumdots GIT_WORK_TREE=$HOME pre-commit install --hook-type pre-commit --hook-type commit-msg
```

---

## 💻 Daily Usage Workflow

Because the repository maps directly to `$HOME`, you never need to copy or symlink files. Use the alias just like standard `git`:

### Public Dotfiles (`bumdots`)

```bash
# Check status of tracked public configuration files
dotfiles status

# Track or stage a public dotfile
dotfiles add ~/.bashrc ~/.gitconfig

# Commit changes (pre-commit quality gates will run automatically)
dotfiles commit -m "feat(shell): add new custom alias"

# Push to GitHub
dotfiles push
```

### Private Overlay Dotfiles (Optional)

If you configure a private overlay repository (with its alias defined inside `~/.bashrc.local`):

```bash
# Check status of private overlay files
dotfiles-priv status

# Stage a private or work-related configuration
dotfiles-priv add ~/.ssh/config.local ~/.gitconfig.local

# Commit private configuration
dotfiles-priv commit -m "chore(ssh): update homelab jump host configuration"

# Push to private remote
dotfiles-priv push
```

---

## 📦 Cloning & Bootstrapping a New Machine

To replicate this environment on a fresh workstation or server:

### 1. Clone the Public Dotfiles

```bash
# Clone as a bare repository
git clone --bare git@github.com:bumuellp/bumdots.git $HOME/repos/bumdots

# Define temporary alias for bootstrapping
alias dotfiles='/usr/bin/git --git-dir=$HOME/repos/bumdots/ --work-tree=$HOME'

# Hide untracked files
dotfiles config --local status.showUntrackedFiles no

# Checkout the files into $HOME (backup conflicting default files if prompted)
dotfiles checkout
```

_If `checkout` reports collisions with default distribution files (like `.bashrc`), move them to a backup folder and re-run `dotfiles checkout`._

### 2. Optional: Clone a Private Overlay Repository

If you maintain a separate private repository for machine-specific secrets and work profiles:

```bash
# Clone private overlay as a bare repository
git clone --bare git@github.com:<username>/<private-dots>.git $HOME/repos/<private-dots>

# Define temporary alias
alias dotfiles-priv='/usr/bin/git --git-dir=$HOME/repos/<private-dots>/ --work-tree=$HOME'

# Hide untracked files
dotfiles-priv config --local status.showUntrackedFiles no

# Checkout private overlay files into $HOME
dotfiles-priv checkout
```

### 3. Install Pre-Commit Hooks

```bash
GIT_DIR=$HOME/repos/bumdots GIT_WORK_TREE=$HOME pre-commit install --hook-type pre-commit --hook-type commit-msg
```

---

## 🔒 Security & Accidental Commit Prevention

This repository includes strict ignore rules in [`.gitignore`](.gitignore) preventing accidental staging of sensitive files:

- **SSH Keys**: Blocks `~/.ssh/id_*`, `~/.ssh/deploy_key*`, and `~/.ssh/known_hosts*` (while allowing `.pub` public keys).
- **CLI Auth Tokens**: Blocks `.config/gh/hosts.yml` and `.config/glab-cli/config.yml`.
- **Histories & Secrets**: Blocks `.bash_history`, `.zsh_history`, and all `.env` files.
