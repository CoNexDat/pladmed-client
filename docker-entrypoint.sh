#!/bin/sh

echo "Setting upload bandwidth limit: $UPLOAD_RATE"

tcset --device eth0 --rate $UPLOAD_RATE --network 192.168.0.235

exec "$@"
