from multiprocessing import Process
from multiprocessing.connection import Client, Listener
from common.operation import Operation
from os import getenv

STOP = 0
NEW_DATA = 1

IN_PROCESS = 0
FINISHED = 1
SENT = 2

address = ('localhost', 6000)

class OperationsManager():
    def __init__(self, storage):
        self.listener = Listener(address, authkey=b'secret password')
        print("Listener created")
        self.listener_conn = None
        self.storage = storage
        self.current_ops = self.storage.read_operations_state()
        self.transmit_manager = None

        print("Starting with: ", self.current_ops)

    def in_process_operations(self):
        operations = []

        for op in self.current_ops:
            if self.current_ops[op] == IN_PROCESS:
                operations.append(op)
        
        return operations        

    def finished_operations(self):
        operations = []

        for op in self.current_ops:
            if self.current_ops[op] == FINISHED:
                operations.append(op)
        
        return operations

    def start(self):
        self.p = Process(target=self.run)
        self.p.start()
        self.listener_conn = self.listener.accept()
        print("Listener conn created")
        
    def stop(self):
        self.listener_conn.send(STOP)
        self.p.join()
        print("Operation manager stopped")

    def run(self):
        print("Running with: ", self.current_ops)
        client = Client(address, authkey=b'secret password')
        print("Client created")

        while client.recv() != STOP:
            [operation_data, status] = client.recv()
            print(f'Got an operation id {operation_data["id"]} with status {status}')

            print(operation_data)

            operation = Operation(
                operation_data["id"],
                operation_data["params"],
                operation_data["cron"],
                operation_data["times_per_minute"],
                operation_data["stop_time"]
            )

            if status == SENT:
                self.delete_operation(operation)
            elif status == FINISHED:
                self.transmit_manager.notify_end_operation(operation)
                self.storage.mark_operation_finished(operation)
            else:
                self.current_ops[operation] = status

            self.save_current_status()

            print("Current ops after: ", self.current_ops)

        print("Operation manager ending its work...")

    def end_operation(self, operation):
        self.listener_conn.send(NEW_DATA)
        self.listener_conn.send([operation.data(), FINISHED])

    def remove_operation(self, operation):
        self.listener_conn.send(NEW_DATA)
        self.listener_conn.send([operation.data(), SENT])

    def save_current_status(self):
        self.storage.save_operations_state(self.current_ops)

    def delete_operation(self, operation):
        self.storage.remove_operation(operation)
        del self.current_ops[operation]
