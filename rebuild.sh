# Load env vars
set -a
source .env
set +a

# Remove all containers and named volumes (claude-config)"
sudo docker compose down -v

# Remove images
sudo docker rmi $(sudo docker images claude-${PROJECT_SLUG}-claude -q)
sudo docker rmi $(sudo docker images claude-${PROJECT_SLUG}-proxy  -q)

# Fresh rebuild without cache
sudo docker compose build --no-cache

# Spinning up!
sudo docker compose up -d
