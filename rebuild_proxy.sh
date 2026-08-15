# Load env vars
set -a
source .env
set +a

# Stop everything
sudo docker compose stop

# Remove container
sudo docker rm proxy-${PROJECT_SLUG}

# Remove image
sudo docker rmi $(sudo docker images claude-${PROJECT_SLUG}-proxy -q)

# Fresh rebuild without cache
sudo docker compose build proxy --no-cache

# Spinning up!
sudo docker compose up -d
