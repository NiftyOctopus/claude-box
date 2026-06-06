# Stop everything
docker compose stop

# Remove container
docker rm claude

# Remove image
docker rmi $(docker images claude-box-claude -q)

# Fresh rebuild without cache
docker compose build claude --no-cache

# Spinning up!
docker compose up -d
