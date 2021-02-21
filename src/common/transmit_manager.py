from multiprocessing import Process, SimpleQueue
from config.connection import RESULT_FOLDER
import subprocess

STOP = 0
NEW_RESULTS = 1

class TransmitManager():#Process):
    def __init__(self, sio, operations_manager):
        #super(Process, self).__init__()

        self.sio = sio
        self.queue = SimpleQueue()
        self.operations_manager = operations_manager
    
    def run(self):
        self.start()

    def start(self):        
        while self.queue.get() != STOP:
            operation = self.queue.get()

            print("Got finished operation: ", operation)

            # Send operation to server
            self.send_results(operation)

            self.operations_manager.remove_operation(operation)

        print("Finalizando...")

    def send_results(self, operation):
        with open(RESULT_FOLDER + "/" + operation, 'rb') as f:
            content = f.read()

            data_to_send = {
                "operation_id": operation,
                "content": content,
                "eof": True
            }

            self.sio.emit("results", data_to_send, namespace='')

    def stop(self):
        self.queue.put(STOP)

    def notify_end_operation(self, op_id):
        self.queue.put(NEW_RESULTS)
        self.queue.put(op_id)
