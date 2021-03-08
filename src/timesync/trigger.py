#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..', 'src')))

from multiprocessing.connection import Client
from sync import SYNC_MESSAGE, SYNC_PASSWORD

port = int(os.getenv('TIME_SYNC_PORT'))


def send_sync_msg_to_app():
    print(f"Triggering sync on {port}")
    address = ('localhost', port)
    conn = Client(address, authkey=SYNC_PASSWORD)
    conn.send(SYNC_MESSAGE)
    conn.close()


send_sync_msg_to_app()
