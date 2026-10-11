# Load env vars
set -a
source .env
set +a

# Move to project directory
cd ~/Dev/claude-${PROJECT_SLUG}

docker compose up -d
docker compose exec claude claude --dangerously-skip-permissions
