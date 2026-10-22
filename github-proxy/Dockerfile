# Small official Python image
FROM python:3.12-alpine

# Copy the proxy code and rules into the image
COPY proxy.py rules.py /app/

# Print logs immediately (no buffer)
# Mainly so print() statements show up right away
ENV PYTHONUNBUFFERED=1

# Don't run as root
USER nobody

EXPOSE 8080

# Run the proxy
CMD ["python", "/app/proxy.py"]