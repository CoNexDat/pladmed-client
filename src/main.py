#!/usr/bin/env python3

from common.client import Client
import socketio
import time

HOST = "http://0.0.0.0:5000"
DELAY_BETWEEN_RETRY = 5

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

@sio.on('connected')
def on_message(data):
    client.on_message(data)

def connect_to_server(host):
    running = True

    while running:
        try:
            sio.connect(host)
            sio.wait
            running = False
        except:
            time.sleep(DELAY_BETWEEN_RETRY)

def main():
    connect_to_server(HOST)

if __name__== "__main__":
	main()
