# Simple Ubuntu image
FROM ubuntu:24.04

# Install dependencies (add more as needed)
# -y: Automatically answer yes to prompts
RUN apt-get update
RUN apt-get install -y curl git
RUN apt-get install -y python3 python3-pip

# We want a non-root user
# We also want the User and Group ID to match the host (avoids perm issues when collaborating on files)
# In many cases we can just use the default ubuntu user
# If not, you might need to create a new user, and perhaps set the IDs explicitly.
USER ubuntu
WORKDIR /home/ubuntu

# Download Claude Code CLI install script (native binary)
# This way we have a record of the version used for this build
RUN curl -fsSLO https://claude.ai/install.sh

# -f:  Treat HTTP errors as failures
# -s:  Silent mode (no progress info)
# -S:  Show error messages
# -sS: Show errors but no other info
# -L:  Follow redirects (important if the file is on a CDN or has moved)
# -O:  Save the file locally

# Install
RUN bash install.sh

# Add to PATH so we can use the claude command
ENV PATH="/home/ubuntu/.local/bin:${PATH}"

# Copy project instructions to the container
COPY --chown=ubuntu:ubuntu CLAUDE.md .claude/CLAUDE.md

# Copy python requirements list to the container
COPY --chown=ubuntu:ubuntu requirements.txt requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt
