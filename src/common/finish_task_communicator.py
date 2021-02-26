from multiprocessing import Process
from multiprocessing.connection import Client
from common.operation import Operation
from common.task import Task
from os import path, getenv
import json

address = ('localhost', int(getenv('FINISH_TASK_PORT')))


class FinishTaskCommunicator:
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
            finished_task_data_str = self.client.recv()
            finished_task_data = json.load(finished_task_data_str)
            operation = Operation(
                finished_task_data["operation"]["id"],
                finished_task_data["operation"]["params"],
                finished_task_data["operation"]["credits"],
                finished_task_data["operation"]["cron"],
                finished_task_data["operation"]["times_per_minute"],
                finished_task_data["operation"]["stop_time"]
            )
            task = Task(
                finished_task_data["task_code"]
            )
            self.communicator.finish_task(operation, task)

