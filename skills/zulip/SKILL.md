---
name: zulip
description: Read and search YourStake's Zulip work chat. Use when the user mentions Zulip, chat, a channel or topic, etc.
---

# Zulip REST API
*Credentials are already in env vars. Never print `ZULIP_API_KEY`!*

| Var             | Value                                   |
|-----------------|-----------------------------------------|
| `ZULIP_SITE`    | `https://zulip.stakedatawerewolf.com`   |
| `ZULIP_EMAIL`   | `bryan-bot@zulip.stakedatawerewolf.com` |
| `ZULIP_API_KEY` | [secret]                                |


## Usage
- Use HTTP Basic auth: `-u "$ZULIP_EMAIL:$ZULIP_API_KEY"`
- Use `curl`
- Use `jq` as needed


## Common Calls

```bash
Z() { curl -s -G -u "$ZULIP_EMAIL:$ZULIP_API_KEY" "$ZULIP_SITE/api/v1/$1" "${@:2}"; }

Z users/me/subscriptions       # Channels the bot can see
Z users                        # All users (names, emails, ids)
Z users/me/<channel_id>/topics # Topics in a channel
```


## Tips
- Paginate older history with `anchor=<oldest id seen>` and `include_anchor=false`.
- Use `apply_markdown=false` to return raw text instead of HTML.
- Read-only by default. Only post messages if Bryan explicitly asks and approves the exact text.
