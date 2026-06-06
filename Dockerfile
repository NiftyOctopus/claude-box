# Simple Ubuntu image
FROM ubuntu:24.04

# Install dependencies (add more as needed)
# -y: Automatically answer yes to prompts
RUN apt-get update
RUN apt-get install -y curl git
# Uncomment if you want Claude to be able to use Python
# RUN apt-get install -y python3 python3-pip python3-venv

# We want a non-root user
# We also want the User and Group ID to match the host (avoids perm issues when collaborating on files)
# In many cases we can just use the default ubuntu user
# If not, you might need to create a new user, and perhaps set the IDs explicitly.
USER ubuntu
WORKDIR /home/ubuntu

# Install Claude Code CLI (native binary)
RUN curl -fsSL https://claude.ai/install.sh | bash

# -f:  Treat HTTP errors as failures
# -s:  Silent mode (no progress info)
# -S:  Show error messages
# -sS: Show errors but no other info
# -L:  Follow redirects (important if the file is on a CDN or has moved)

# Add to PATH so we can use the claude command
ENV PATH="/home/ubuntu/.local/bin:${PATH}"

# Copy project instructions to the container
COPY --chown=ubuntu:ubuntu CLAUDE.md .claude/CLAUDE.md

# Create Python virtual env
# Uncomment if you are using Python
# RUN python3 -m venv /home/ubuntu/.venv

# Ensures we install packages in the venv
# We cannot use the source command in a Dockerfile because each RUN command is a separate shell.
# Instead we modify PATH so venv/bin is first, ensuring pip is run inside the venv.
ENV PATH="/home/ubuntu/.venv/bin:$PATH"

# Install Python dependencies (if needed)
# RUN pip install requests
