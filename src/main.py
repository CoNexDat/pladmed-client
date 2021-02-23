#!/usr/bin/env python3

from common.client import Client
from common.storage import Storage
import config.connection as config
import timesync.sync as timesync
import socketio
import time
import os
from multiprocessing import Process
from common.operations_manager import OperationsManager


def config_connection(client):
    processes = []

    @client.sio.event
    def connect():
        client.connect()

        #p = Process(target=transmitter_process, args=(client, ))
        # p.start()
        # processes.append(p)

    @client.sio.event
    def connect_error(message):
        print("Conn error: ", message)

    @client.sio.event
    def disconnect():
        # This is only called for the process who contains all the other processes
        client.disconnect()

        # for p in processes:
        #    print("Waiting for processes")
        #    p.join()

        print("All processes finished")

    @client.sio.on('traceroute')
    def on_traceroute(data):
        print("Traceroute received")
        client.traceroute(data["_id"], data["params"])

    @client.sio.on('ping')
    def on_ping(data):
        client.ping(data["_id"], data["params"])


def connect_to_server(client):
    token = os.getenv('TOKEN', 'token')

    running = True

    config_connection(client)

    while running:
        try:
            client.sio.connect(config.HOST + "?token=" + token)

            client.sio.wait

            running = False
        except:
            time.sleep(config.DELAY_BETWEEN_RETRY)


def main():
    sio = socketio.Client(engineio_logger=True,
                          reconnection=True, reconnection_attempts=0)

    storage = Storage(
        config.RESULT_FOLDER,
        config.STATE_FILE,
        config.TMP_FOLDER
    )

    operations_manager = OperationsManager(storage)

    client = Client(sio, storage, operations_manager)

    connect_to_server(client)
    timesync.listen()


if __name__ == "__main__":
    main()
