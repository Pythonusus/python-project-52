#!/usr/bin/env bash

# Install dependencies
make install

# Collect static files
make static

# Apply migrations
make migrate

# Create a superuser
make createsuperuser
