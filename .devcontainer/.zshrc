export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="robbyrussell"

plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
)

fpath+=${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions/src

. $ZSH/oh-my-zsh.sh
. "$HOME/.atuin/bin/env"
. "$HOME/.cargo/env"
. "$HOME/.rye/env" || true

eval "$(atuin init zsh)"

export PATH="$PATH:/root/.local/bin"

alias exa=eza
