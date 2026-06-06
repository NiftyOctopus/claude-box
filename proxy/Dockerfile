# Alpine is a lightweight Linux distro
FROM alpine:3.23

# Install tinyproxy
# https://tinyproxy.github.io
RUN apk add --no-cache tinyproxy

# Install curl for healthcheck and debugging
RUN apk add --no-cache curl

# Copy config file over to container
COPY tinyproxy.conf /etc/tinyproxy/tinyproxy.conf

# Expose the default tinyproxy port
EXPOSE 8888

# Start
CMD ["tinyproxy", "-d", "-c", "/etc/tinyproxy/tinyproxy.conf"]

# -d: Run in the foreground (important for Docker)
# -c: Specify config file path