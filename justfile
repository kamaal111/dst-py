set export

JWT_ALGORITHM := "HS256"
JWT_SECRET_KEY := "not_so_secure_secret"
JWT_EXPIRE_MINUTES := "30"
DATABASE_URL := "sqlite:///database.db"

# List available commands
default:
    just --list --unsorted

# Run server
run:
    docker compose up

# Run server detached
run-d:
    docker compose up -d

# Tear down server
tear:
    docker compose down

# Run local server
run-local: prepare
    #!/bin/zsh

    . .venv/bin/activate
    fastapi dev src/dst_py/main.py

# Test
test: prepare
    #!/bin/zsh

    . .venv/bin/activate
    pytest

# Build container
build:
    docker build -t dst-py .

# Test with code coverage
test-cov:
    #!/bin/zsh

    . .venv/bin/activate
    pytest --cov=src/dst_py tests/

# Lint code
lint:
    #!/bin/zsh

    . .venv/bin/activate
    ruff check .

# Lint and fix any issues that can be fixed automatically
lint-fix:
    #!/bin/zsh

    . .venv/bin/activate
    ruff check . --fix

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
