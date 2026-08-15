# Load env vars
set -a
source .env
set +a

# Stop everything
sudo docker compose stop

# Remove container
sudo docker rm claude-${PROJECT_SLUG}

# Remove image
sudo docker rmi $(sudo docker images claude-${PROJECT_SLUG}-claude -q)

# Fresh rebuild without cache
sudo docker compose build claude --no-cache

# Spinning up!
sudo docker compose up -d
