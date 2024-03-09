# Changelog Generator Script

## Overview

This changelog generator script is designed to create a structured changelog based on commit messages from a Git repository. It uses the Conventional Commits specification to categorize commits into various types such as features, bug fixes, documentation updates, etc. The script can operate in two modes: 'simple' for a concise summary, and 'full' for detailed release notes including descriptions and links to pull requests.

## Task Description

The task involves creating an automated script that:

- Extracts git commit messages between specified start and end commit IDs.
- Categorizes commit messages according to the Conventional Commits standard.
- Fetches associated Pull Request details from GitHub using the GitHub API.
- Generates a changelog in Markdown format with categorized commits and PR details.
- Optionally, the script can be integrated into a CI/CD pipeline for automatic changelog updates.

## How to Run the Script

1. **Set Up Environment Variables (Recommended Method)**
   
   For security reasons, it is recommended to use environment variables to store sensitive information such as your GitHub Personal Access Token (PAT). To set up an environment variable:

   ```sh
   export GITHUB_TOKEN='your_github_personal_access_token_here'

   
#### Usage Instructions
1. Ensure you have Python installed (recommended version: Python 3.6 or higher).
2. Clone the repository containing your project.
3. Navigate to the directory containing the scripts.
4. Set up the environment variable for your GitHub token as mentioned above.
5. Run the script using the following command:

```bash
python script_name.py
```

Replace script_name.py with the name of the script you want to execute (main.py in this case).

### Dependencies
This script has the following dependencies:

requests library for making HTTP requests to the GitHub API.

### System Requirements
Required Python version: Python 3.6 or higher.
Supported Operating Systems: Any OS that supports Python (Windows, macOS, Linux).
