# Load env vars
set -a
source .env
set +a

# Stop everything
sudo docker compose stop

# Remove container
sudo docker rm github-proxy-${PROJECT_SLUG}

# Remove image
sudo docker rmi $(sudo docker images claude-${PROJECT_SLUG}-github-proxy -q)

# Fresh rebuild without cache
sudo docker compose build github-proxy --no-cache

# Spinning up!
sudo docker compose up -d
