# Load env vars
set -a
source .env
set +a

# Stop everything
docker compose stop

# Remove container
docker rm proxy-${PROJECT_SLUG}

# Remove image
docker rmi $(sudo docker images claude-${PROJECT_SLUG}-proxy -q)

# Fresh rebuild without cache
docker compose build proxy --no-cache

# Spinning up!
docker compose up -d
