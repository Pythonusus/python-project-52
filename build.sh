#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install only production dependencies
make install-prod

# Collect static files
make static

# Apply migrations
make migrate
