#!/bin/bash

echo "🚀 Starting CineVault with Docker..."

if [ ! -f .env ]; then
  echo "⚠️  .env file not found. Creating from .env.example"
  cp .env.example .env
  echo "👉 Edit .env with secure passwords before production use."
fi

docker-compose up --build