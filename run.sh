#!/bin/bash
# Vectara Workspace Inspector Runner
# This script activates the virtual environment and runs the workspace inspector

# Activate the virtual environment
source .venv/bin/activate

# Run the inspector with any passed arguments
python vectara_inspector.py "$@"
