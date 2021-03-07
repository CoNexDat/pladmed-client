from multiprocessing import Process
from multiprocessing.connection import Listener
from common.operation import Operation
from os import getenv
import json

address = ('localhost', int(getenv('FINISH_OPERATION_PORT')))


class FinishOperationCommunicator:
    def __init__(self, communicator):
        self.communicator = communicator
        self.listener = Listener(address)
        self.processes = []

    def start(self):
        self.p = Process(target=self.run)
        self.p.start()

    def stop(self):
        self.p.join()
        print("StopperCommunicator manager stopped")

    def run(self):
        while True:
            self.remove_finished()

            conn = self.listener.accept()

            p = Process(target=self.receive_data, args=(conn, ))

            self.processes.append(p)
            p.start()

    def receive_data(self, conn):
        operation_data_str = conn.recv()

        operation_data = json.loads(operation_data_str)

        operation = Operation(
            operation_data["id"],
            operation_data["params"],
            operation_data["credits"],
            operation_data["cron"],
            operation_data["times_per_minute"],
            operation_data["stop_time"],
            operation_data["binary"]
        )

        self.communicator.finish_operation(operation)

        conn.close()

    def remove_finished(self):
        for p in self.processes:
            if not p.is_alive():
                print("Process finished")
                self.processes.remove(p)
