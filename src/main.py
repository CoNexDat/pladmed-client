#!/usr/bin/env python3

from common.client import Client
import config.connection as config
import socketio
import time

sio = socketio.Client(engineio_logger=True, reconnection=True, reconnection_attempts=0)
client = Client()

@sio.event
def connect():
    client.connect()

@sio.event
def connect_error(message):
    print("Conn error: ", message)

@sio.event
def disconnect():
    client.disconnect()

@sio.on('operation')
def on_traceroute(data):
    client.traceroute(data["params"])

def connect_to_server():
    running = True

    while running:
        try:
            sio.connect(config.HOST)
            sio.wait
            running = False
        except:
            time.sleep(config.DELAY_BETWEEN_RETRY)

def main():
    connect_to_server()

if __name__== "__main__":
	main()
