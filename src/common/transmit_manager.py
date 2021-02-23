from multiprocessing import Process, SimpleQueue
from config.connection import RESULT_FOLDER
import subprocess
from common.operation import Operation

STOP = 0
NEW_RESULTS = 1

class TransmitManager():
    def __init__(self, sio, storage, operations_manager):
        self.sio = sio
        self.queue = SimpleQueue()
        self.storage = storage
        self.operations_manager = operations_manager
    
    def run(self):
        self.start()

    def start(self):        
        while self.queue.get() != STOP:
            operation_data = self.queue.get()

            operation = Operation(
                operation_data["id"],
                operation_data["params"],
                operation_data["unique_code"]
            )

            print("Got finished operation: ", operation)

            def ack(operation_id):
                # If operation was successfully saved in the server
                if operation_id == operation.id:
                    self.operations_manager.remove_operation(operation)

            # Send operation to server
            self.send_results(operation, ack)

        print("Transmit manager ending its work...")

    def send_results(self, operation, callback):
        filename = self.storage.operation_filename(operation)

        with open(filename, 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation.id,
                "content": content,
                "unique_code": operation.unique_code
            }

            self.sio.emit(
                "results",
                data_to_send,
                namespace='',
                callback=callback
            )

    def stop(self):
        self.queue.put(STOP)

    def notify_end_operation(self, operation):
        self.queue.put(NEW_RESULTS)
        self.queue.put(operation.data())
