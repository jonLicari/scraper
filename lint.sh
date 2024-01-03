#!/bin/bash

# Ensure script has execute permissions
chmod +x "$0"

# Check if Black is installed
if ! command -v black &> /dev/null
then
    echo "Error: Black is not installed. Installing via pip3..."
    pip3 install black

    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Black. Please install it manually using 'pip install black'."
        exit 1
    fi
fi

# Run Black on Python files
echo "Running Black..."
python3 -m black .

# Add other linters or formatters as needed
# For example, you can add Flake8 for more comprehensive linting
# echo "Running Flake8..."
# flake8 .

echo "Linting complete."
