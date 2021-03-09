from multiprocessing import Process, SimpleQueue
from config.connection import RESULT_FOLDER
import subprocess
from common.operation import Operation, SCAMPER_BINARY
import os
from common.task import Task
from common.communicator import (
    STOP
)


class TransmitManager():
    def __init__(self, sender, storage, communicator):
        self.sender = sender
        self.storage = storage
        self.communicator = communicator

    def run(self):
        self.start()

    def start(self):
        data = self.communicator.read_transmit()

        while data[0] != STOP:
            operation_data = data[1]
            task_data = data[2]

            task = Task(task_data["code"])

            operation = Operation(
                operation_data["id"],
                operation_data["params"],
                operation_data["credits"],
                operation_data["cron"],
                operation_data["times_per_minute"],
                operation_data["stop_time"],
                operation_data["binary"]
            )

            print("Got finished task: ", task.code,
                  " for operation: ", operation.id)

            def ack(operation_id):
                # If operation was successfully saved in the server
                if operation_id == operation.id:
                    print("Successfully sent task: ", task.code,
                          " for operation: ", operation.id)
                    self.communicator.sent_task(operation, task)

            # Send operation to server
            self.send_results(operation, task, ack)

            data = self.communicator.read_transmit()

        print("Transmit manager ending its work...")

    def send_results(self, operation, task, callback):
        filename = self.storage.operation_filename(task)

        print("Sending file size: ", os.path.getsize(filename))

        with open(filename, 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation.id,
                "content": content,
                "unique_code": task.code,
                "format": "warts" if operation.binary == SCAMPER_BINARY else "gzip"
            }

            self.sender.emit(
                "results",
                data_to_send,
                callback=callback
            )

    def stop(self):
        self.communicator.stop_transmit()
