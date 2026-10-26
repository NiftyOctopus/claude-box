---
name: github
description: Query GitHub for YourStake repo info via the local GitHub proxy. Use when the user mentions GitHub, a PR or Issue number, code review, etc.
---

## Access via Proxy
- The CLI is not installed, and the regular proxy blocks direct calls to the API.
- You must use our custom local proxy meant specifically for GitHub.

| Host                           | Use for         |
|--------------------------------|-----------------|
| `http://api.github-proxy:8080` | REST API (curl) |
| `http://git.github-proxy:8080` | Git only        |

*No auth header is needed since the proxy injects credentials*


## Repos

| Repo              | Contains                     |
|-------------------|------------------------------|
| `YourStake/stake` | YourStake app code, PRs, etc |
| `YourStake/hub`   | Issues only                  |

*FYI there is a local (read-only) clone at `/home/ubuntu/code`*


## Contributors
Team GitHub usernames are in `/wiki/yourstake-team.md`


## Common Calls

```bash
API=http://api.github-proxy:8080/repos/YourStake/stake

curl -s "$API/pulls?state=open&per_page=50"  # Open PRs
curl -s "$API/pulls/9123"                    # PR details
curl -s "$API/pulls/9123/files"              # Changed files
curl -s "$API/pulls/9123/reviews"            # Reviews
curl -s "$API/pulls/9123/comments"           # Inline review comments
curl -s "$API/issues/1234/comments"          # Conversation comments
curl -s "$API/issues?state=open"             # Open issues
curl -s "$API/commits?sha=main&per_page=20"  # Recent commits
```


## Tips
- Use `jq` as needed for more complex transforms.
- Lists are paginated. Use `per_page` (max 100) and `page`.
- Treat GitHub as read-only unless Bryan explicitly asks you to post. Comments notify people.