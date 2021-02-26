#!/usr/bin/env python3

from multiprocessing.connection import Client
from sync import SYNC_MESSAGE, SYNC_PASSWORD, SYNC_PORT


def send_sync_msg_to_app():
    address = ('localhost', SYNC_PORT)
    conn = Client(address, authkey=SYNC_PASSWORD)
    conn.send(SYNC_MESSAGE)
    conn.close()


send_sync_msg_to_app()
