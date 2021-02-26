from multiprocessing import Process, SimpleQueue
from config.connection import RESULT_FOLDER
import subprocess
from common.operation import Operation
import os

STOP = 0
NEW_RESULTS = 1

class TransmitManager():
    def __init__(self, sio, storage, communicator):
        self.sio = sio
        self.storage = storage
        self.communicator = communicator
    
    def run(self):
        self.start()

    def start(self):        
        data = self.communicator.read_transmit()

        while data[0] != STOP:
            operation_data = data[1]
            task_code = data[2]

            operation = Operation(
                operation_data["id"],
                operation_data["params"],
                operation_data["credits"],
                operation_data["cron"],
                operation_data["times_per_minute"],
                operation_data["stop_time"]
            )

            print("Got finished task: ", task_code, " for operation: ", operation.id)

            def ack(operation_id):
                # If operation was successfully saved in the server
                if operation_id == operation.id:
                    print("Successfully sent task: ", task_code, " for operation: ", operation.id)
                    self.communicator.sent_task(operation, task_code)

            # Send operation to server
            self.send_results(operation, task_code, ack)

            data = self.communicator.read_transmit()

        print("Transmit manager ending its work...")

    def send_results(self, operation, task_code, callback):
        filename = self.storage.operation_filename(task_code)

        print("Sending file size: ", os.path.getsize(filename))

        with open(filename, 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation.id,
                "content": content,
                "unique_code": task_code
            }

            self.sio.emit(
                "results",
                data_to_send,
                namespace='',
                callback=callback
            )

    def stop(self):
        self.communicator.stop_transmit()
