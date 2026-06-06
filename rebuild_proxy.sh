# Stop everything
docker compose stop

# Remove container
docker rm proxy

# Remove image
docker rmi $(docker images claude-box-proxy -q)

# Fresh rebuild without cache
docker compose build proxy --no-cache

# Spinning up!
docker compose up -d
