#!/bin/sh

echo "Starting crond service..."
crond &

exec "$@"