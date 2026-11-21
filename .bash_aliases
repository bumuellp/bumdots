# Dotfiles repository alias
alias dotfiles='/usr/bin/git --git-dir=$HOME/repos/bumdots/ --work-tree=$HOME'

# Easy one command for update, upgrade and dist-upgrade.
# Requires usually sudo
alias update='sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y && sudo apt autoremove -y'
