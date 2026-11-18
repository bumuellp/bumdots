#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"

for item in \
  .bashrc \
  .bash_logout \
  .profile \
  .gitconfig \
  .gitattributes \
  .editorconfig \
  .prompts \
  .agents \
  .yamllint \
  .trivyignore \
  trivy.yaml \
  .config/gh/config.yml \
  .config/git/config-github \
  .config/glab-cli/aliases.yml \
  .config/opencode/opencode.json \
  .gemini/config/hooks.json \
  .gemini/config/rules \
  .gemini/config/secret_guard.py \
  .gemini/skills; do
  if [ -e "$DOTFILES_DIR/$item" ]; then
    mkdir -p "$(dirname "$HOME/$item")"
    rm -rf "$HOME/$item"
    ln -s "$DOTFILES_DIR/$item" "$HOME/$item"
  fi
done

if ! command -v agy >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/agy" ]; then
  curl -fsSL https://antigravity.google/cli/install.sh | bash
fi

if [ -x "$HOME/.local/bin/agy" ] && [ ! -e /usr/local/bin/agy ]; then
  sudo ln -sf "$HOME/.local/bin/agy" /usr/local/bin/agy 2>/dev/null || ln -sf "$HOME/.local/bin/agy" /usr/local/bin/agy 2>/dev/null || true
fi
