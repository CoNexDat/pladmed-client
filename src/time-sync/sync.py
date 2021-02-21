#!/usr/bin/env python3

import os

ntp_server_url = os.getenv('NTP_SERVER', 'ntp_server')
print(f"Will sync with ntp server at {ntp_server_url}")
