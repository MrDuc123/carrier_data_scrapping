#!/bin/bash
set -e

# Check for Poetry installation
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    # Add Poetry to the PATH for the current session
    export PATH="$HOME/.local/bin:$PATH"
    echo "Poetry installed at $HOME/.local/bin."
    
    # Persist the PATH change by appending it to ~/.bashrc if it's not already there
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo "Added Poetry to PATH in ~/.bashrc."
    fi
else
    echo "Poetry is already installed."
fi

# Configure Poetry to create virtual environments in the project directory (.venv)
echo "Configuring Poetry to create the virtual environment in the project directory..."
poetry config virtualenvs.in-project true

# Run poetry install to create the .venv folder and install dependencies
echo "Running 'poetry install' to set up the environment..."
poetry install --no-root

echo "Setup complete. Your virtual environment has been created in the .venv directory."
# echo "To activate it, run 'poetry shell'."
