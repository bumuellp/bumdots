#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"

for item in .bashrc .bash_logout .profile .gitconfig .gitattributes .editorconfig .gemini .config .prompts .agents .yamllint .trivyignore trivy.yaml; do
  if [ -e "$DOTFILES_DIR/$item" ]; then
    rm -rf "$HOME/$item"
    ln -s "$DOTFILES_DIR/$item" "$HOME/$item"
  fi
done

if ! command -v agy >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/agy" ]; then
  curl -fsSL https://antigravity.google/cli/install.sh | bash
fi
