from multiprocessing import Process
from multiprocessing.connection import Listener
from common.operation import Operation
from common.task import Task
from os import path, getenv
import json

address = ('localhost', int(getenv('FINISH_TASK_PORT')))


class FinishTaskCommunicator:
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
        finished_task_data_str = conn.recv()

        finished_task_data = json.loads(finished_task_data_str)

        operation = Operation(
            finished_task_data["operation"]["id"],
            finished_task_data["operation"]["params"],
            finished_task_data["operation"]["credits"],
            finished_task_data["operation"]["cron"],
            finished_task_data["operation"]["times_per_minute"],
            finished_task_data["operation"]["stop_time"],
            finished_task_data["operation"]["binary"]
        )

        task = Task(
            finished_task_data["task"]["code"]
        )

        self.communicator.finish_task(operation, task)

        conn.close()

    def remove_finished(self):
        for p in self.processes:
            if not p.is_alive():
                print("Process finished")
                self.processes.remove(p)
