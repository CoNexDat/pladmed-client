#!/usr/bin/env python3

from common.client import Client
from common.storage import Storage
import config.connection as config
import socketio
import time
import os
import subprocess

sio = socketio.Client(engineio_logger=True, reconnection=True, reconnection_attempts=0)

storage = Storage(config.RESULT_FOLDER)
client = Client(storage)


@sio.event
def connect():
    client.connect()


@sio.event
def connect_error(message):
    print("Conn error: ", message)


@sio.event
def disconnect():
    client.disconnect()


@sio.on('traceroute')
def on_traceroute(data):
    client.traceroute(data["_id"], data["params"])


@sio.on('ping')
def on_ping(data):
    client.ping(data["_id"], data["params"])


def connect_to_server():
    subprocess.run("crond") # Starts crontab
    token = os.getenv('TOKEN', 'token')

    running = True

    while running:
        try:
            sio.connect(config.HOST + "?token=" + token)
            sio.wait
            running = False
        except:
            time.sleep(config.DELAY_BETWEEN_RETRY)


def main():
    connect_to_server()


if __name__ == "__main__":
    main()
