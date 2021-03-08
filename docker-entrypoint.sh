#!/bin/sh

echo "Setting upload bandwidth limit $UPLOAD_RATE for uploads bound to $BACKEND_IP"

tcset --device eth0 --rate $UPLOAD_RATE --network $BACKEND_IP

echo "Starting crond service..."
crond &

exec "$@"
