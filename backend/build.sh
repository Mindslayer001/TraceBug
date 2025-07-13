#!/usr/bin/env bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies
poetry config virtualenvs.create false  # So Render uses the global environment
poetry install --no-interaction --no-root
