"""
Allowlist rules for the GitHub proxy
Step 2a and 2c: Repo check and safe path check

Not yet checked: HTTP method, specific endpoints (rules.toml)
"""


def load_repos(repos_path):
    repos = set()
    with open(repos_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                repos.add(line.lower())

    return repos


def get_repo(host, path):
    """
    Pull owner/repo out of the path (or return None)
    api.github-proxy:  /repos/owner/repo/
    git.github-proxy:  /owner/repo.git/
    """

    path  = path.split('?')[0]         # Drop query string if it exists
    parts = path.strip('/').split('/') # Split path segments

    # GitHub API
    if host == 'api.github-proxy':
        if len(parts) < 3 or parts[0] != 'repos':
            return None

        owner = parts[1]
        repo  = parts[2]
        return f'{owner}/{repo}'.lower()

    # Git operations
    if host == 'git.github-proxy':
        if len(parts) < 2: return None

        owner = parts[0]
        repo  = parts[1].removesuffix('.git')
        return f'{owner}/{repo}'.lower()
    
    return None


BAD_PATH_PARTS = [
    '..',  # Jump to parent folder
    '//',  # Empty segment: Shifts which part is read as owner/repo
    '\\',  # Backslash: Some servers treat it like /
    '%2e', # Hidden '.'
    '%2f', # Hidden '/'
    '%5c', # Hidden '\'
    '%00', # Null byte: Can cut the path short in some systems
] 

def check_path_safety(raw_path):
    """Prevent sneaky path tricks from bypassing allowed repos"""

    # Block absolute URLs
    if not raw_path.startswith('/'):
        return 'Path must start with /'

    # Drop query string (we are just checking path)
    path = raw_path.split('?')[0].lower()
    
    for bad in BAD_PATH_PARTS:
        if bad in path:
            return f'Path contains suspicious character {bad}'
            
    return None


def check(repos, host_header, path):
    host = host_header.split(':')[0].lower() # Drop port number

    unsafe = check_path_safety(path)
    if unsafe: return False, unsafe

    repo = get_repo(host, path)

    if repo is None:
        allowed = False
        reason  = 'No repo in path (or unknown host)'
        return allowed, reason
    
    if repo not in repos:
        allowed = False
        reason  = f'Repo {repo} not allowed'
        return allowed, reason

    return True, 'OK'
