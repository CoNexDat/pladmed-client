from multiprocessing import Process
from multiprocessing.connection import Client
from common.operation import Operation
from os import getenv
import json

address = ('localhost', int(getenv('FINISH_OPERATION_PORT')))


class FinishOperationCommunicator:
    def __init__(self, communicator):
        self.communicator = communicator
        self.client = Client(address)

    def start(self):
        self.p = Process(target=self.run)
        self.p.start()

    def stop(self):
        self.p.join()
        print("StopperCommunicator manager stopped")

    def run(self):
        while True:
            operation_data_str = self.client.recv()
            operation_data = json.load(operation_data_str)
            operation = Operation(
                operation_data["id"],
                operation_data["params"],
                operation_data["credits"],
                operation_data["cron"],
                operation_data["times_per_minute"],
                operation_data["stop_time"]
            )
            self.communicator.finish_operation(operation)

