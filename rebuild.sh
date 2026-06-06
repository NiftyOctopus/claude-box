# Remove all containers and named volumes (claude-config)"
docker compose down -v

# Remove images
docker rmi $(docker images claude-box-claude -q)
docker rmi $(docker images claude-box-proxy  -q)

# Fresh rebuild without cache
docker compose build --no-cache

# Spinning up!
docker compose up -d
