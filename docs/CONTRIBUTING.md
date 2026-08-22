# Contributing to HoneyRoot-X

First off, thank you for considering contributing to HoneyRoot-X! 

## Development Setup
1. Clone the repo and create a virtual environment (`python -m venv venv`).
2. Install dependencies: `pip install -r requirements.txt` and `pip install pytest flake8`.
3. Make your changes in a new branch.

## Testing Your Changes
Before submitting a pull request, please ensure all tests pass and the code is linted:
\`\`\`bash
make test
\`\`\`
*(This will run `pytest` and `flake8` against the core directories).*

## Adding New Commands to the Fake Shell
If you are modifying `core/fake_shell.py` to support new Linux commands:
* Keep responses as authentic as possible to Ubuntu 22.04 LTS.
* Ensure the command is logged to `logger.py` if it represents an IoC (Indicator of Compromise).
