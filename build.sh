#!/usr/bin/env bash

# Install only production dependencies
make install-prod

# Collect static files
make static

# Apply migrations
make migrate

# Create a superuser
make createsuperuser
