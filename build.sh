#!/bin/bash
# Render build script

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p secrets

# Create default config.json if it doesn't exist
if [ ! -f config.json ]; then
  echo "{}" > config.json
fi

echo "Build completed successfully!"
