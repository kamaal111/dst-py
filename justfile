set export

# List available commands
default:
    just --list --unsorted

run:
    #!/bin/zsh

    . .venv/bin/activate
    fastapi dev main.py

# Prepare project to work with
prepare: install-modules

# Bootstrap project
bootstrap: install-rye prepare
    #!/bin/zsh

    just setup-pre-commit

# Set up dev container. This step runs after building the dev container
post-dev-container-create:
    just .devcontainer/post-create
    just bootstrap

# Install modules
install-modules:
    #!/bin/zsh

    . ~/.zshrc

    rye sync

[private]
setup-pre-commit:
    #!/bin/zsh

    . .venv/bin/activate
    pre-commit install

[private]
install-rye:
    #!/bin/zsh

    curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes"  bash

    . ~/.zshrc

    mkdir -p ~/.zfunc
    rye self completion -s zsh > ~/.zfunc/_rye

    if [[ -n $ZSH_CUSTOM ]]
    then
        mkdir -p $ZSH_CUSTOM/plugins/rye
        rye self completion -s zsh > $ZSH_CUSTOM/plugins/rye/_rye
    fi