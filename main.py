import subprocess
import re
import requests

# Configuration
start_commit_id = '17884628603c13c19ba11cbd5eafeb10955870db'
end_commit_id = '3c70fec324e36be898da18cee54d512535c6ecac'
github_token = 'token_here'
owner = 'synfig'
repo = 'synfig'
mode = 'simple'  # Use 'simple' for weekly notes or 'full' for detailed release notes
# Emoji dictionary for commit types
commit_emojis = {
    'feat': ':sparkles:',
    'fix': ':bug:',
    'docs': ':books:',
    'style': ':gem:',
    'refactor': ':recycle:',
    'perf': ':rocket:',
    'test': ':white_check_mark:',
    'build': ':package:',
    'ci': ':construction_worker_man:',
    'chore': ':wrench:',
    'others': ':memo:'
}

def run_git_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    if result.returncode != 0:
        raise Exception(f"Error executing git command: {result.stderr}")
    return result.stdout.strip()

def extract_commits(start_commit_id, end_commit_id):
    command = f"git log {start_commit_id}^..{end_commit_id} --pretty=format:'%H %s'"
    log_output = run_git_command(command)
    commit_pattern = re.compile(r"^(?P<hash>[a-f0-9]+) (?P<type>\w+)(\(\w+\))?!?: (?P<message>.+)( \(#\d+\))?$")
    merge_commit_pattern = re.compile(r'^Merge branch ')
    commits = []

    for line in log_output.split('\n'):
        if merge_commit_pattern.search(line):
            # This is a merge commit, handle it differently if needed
            commit_type = 'merge'
            commit_message = line
        else:
            # This is a normal commit, handle according to Conventional Commits
            match = commit_pattern.match(line)
            if match:
                commit_type = match.group('type')
                commit_message = match.group('message')
            else:
                commit_type = 'others'
                commit_message = line  # The full commit message is used if it doesn't match the pattern

        commits.append({
            'hash': line.split(' ', 1)[0],
            'type': commit_type,
            'message': commit_message
        })
    return commits

def fetch_pr_details(pr_id, mode):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(url, headers=headers)
    
    # Check if the response was successful
    if response.status_code == 200:
        pr_data = response.json()
        
        # For 'simple' mode, only the PR title is required
        if mode == 'simple':
            return f"{pr_data.get('title', 'No title')} (#{pr_id})"
        else:
            # For 'full' mode, return title, body, and URL if available
            # If body is None or empty, default to 'No description provided'
            body = pr_data.get('body', 'No description provided')
            # Split the body on newlines and take the first line if body is not 'None'
            body_first_line = body.split('\n')[0] if body else 'No description provided'
            return f"{pr_data.get('title', 'No title')} (#{pr_id}): {body_first_line} - {pr_data.get('html_url', 'No URL')}"
    
    # If the response failed, return an error message with the status code
    error_message = response.json().get('message', 'No error message provided')
    return f"PR details not found for #{pr_id}: {response.status_code} Error - {error_message}"

def categorize_commits(commits, mode):
    categorized_commits = {emoji: [] for emoji in commit_emojis.values()}
    
    for commit in commits:
        commit_type = commit['type']
        emoji = commit_emojis.get(commit_type, commit_emojis['others'])
        commit_message = f"{emoji} {commit['message']} ({commit['hash']})"
        pr_id_search = re.search(r'\(#(\d+)\)$', commit['message'])
        pr_details = ''
        if pr_id_search:
            pr_id = pr_id_search.group(1)
            if pr_id:  # Ensure PR ID is not None
                pr_details = fetch_pr_details(pr_id, mode)
        commit_message += f" - {pr_details}"
        categorized_commits[emoji].append(commit_message)
    
    return categorized_commits

def generate_changelog(categorized_commits):
    changelog = "# Changelog\n\n"
    for emoji, messages in categorized_commits.items():
        if messages:
            changelog += f"## {emoji}\n"
            for message in messages:
                changelog += f"{message}\n"
            changelog += "\n"
    return changelog

if __name__ == "__main__":
    commits = extract_commits(start_commit_id, end_commit_id)
    categorized_commits = categorize_commits(commits, mode)
    changelog = generate_changelog(categorized_commits)
    print(changelog)
    with open('CHANGELOG.md', 'w') as file:
        file.write(changelog)