from multiprocessing import Process, SimpleQueue
from common.operation import Operation
from common.task import Task
import subprocess
from common.communicator import (
    STOP,
    NEW_DATA,
    IN_PROCESS,
    FINISHED,
    TASK_FINISHED,
    TASK_SENT,
    CREDITS
)
import uuid

class OperationsManager():
    def __init__(self, storage, communicator):
        self.storage = storage
        self.communicator = communicator
        self.current_ops = self.storage.read_operations_state()

        #TODO: Remove
        self.processes = []

        self.recover_state()

    def actual_credits(self):
        total_credits = 0

        for operation in self.current_ops.values():
            total_credits += operation.credits
        
        return total_credits

    def recover_state(self):
        for operation in self.current_ops.values():
            if operation.status == IN_PROCESS:
                self.schedule_operation(operation)

        for operation in list(self.current_ops.values()):
            self.check_operation_finished(operation)

        for operation in self.current_ops.values():
            finished_tasks = operation.finished_tasks()

            for task in finished_tasks:
                self.communicator.notify_end_task(operation, task)   

    def start(self):
        self.current_ops = self.storage.read_operations_state()
        
        self.p = Process(target=self.run)
        self.p.start()
        
    def stop(self):
        self.communicator.stop_operations()
        self.p.join()

        for p in self.processes:
            p.join()

        print("Operation manager stopped")

    def run(self):
        print("Running with: ", self.current_ops)

        data = self.communicator.read_operations()

        while data[0] != STOP:
            status = data[1]

            if status == CREDITS:
                self.communicator.notify_current_credits(self.actual_credits())
            else:
                operation_data = data[2]
                op_id = operation_data["id"]

                if status == IN_PROCESS:
                    print("New operation income")
                    operation = Operation(
                        operation_data["id"],
                        operation_data["params"],
                        operation_data["credits"]
                    )

                    self.schedule_operation(operation)
                    self.current_ops[op_id] = operation

                elif status == TASK_FINISHED:
                    print("New task finished income")
                    task_data = data[3]

                    task = Task(task_data["code"])

                    self.storage.mark_task_finished(task)
                    self.current_ops[op_id].add_task(task)
                    self.communicator.notify_end_task(self.current_ops[op_id], task)

                elif status == FINISHED:
                    print("Operation finished")

                    self.current_ops[op_id].status = FINISHED
                    self.check_operation_finished(self.current_ops[op_id])

                elif status == TASK_SENT:
                    print("Task sent income")
                    task_data = data[3]

                    task = Task(task_data["code"])

                    self.current_ops[op_id].update_task(task, TASK_SENT)
                    # Save so that a sent task doesn't re-send in case of crash
                    self.save_current_status()
                    self.storage.remove_task(task)
                    self.check_operation_finished(self.current_ops[op_id])

                self.save_current_status()
                
                print("Current ops after: ", self.current_ops)

            data = self.communicator.read_operations()

        print("Operation manager ending its work...")

    def add_operation(self, operation):
        self.communicator.add_operation(operation)

    def check_operation_finished(self, operation):
        if operation.status == FINISHED and operation.all_task_sent():
            del self.current_ops[operation.id]

    def save_current_status(self):
        self.storage.save_operations_state(self.current_ops)

    def schedule_operation(self, operation):
        # TODO: Schedule in Cron...
        # Temporary execute scamper here
        print("Scheduling: ", operation)
        p = Process(target=self.execute_scamper, args=(operation, ))
        p.start()
        self.processes.append(p)

    def execute_scamper(self, operation):        
        for i in range(0, 5):
            task = Task(str(uuid.uuid4()))

            subprocess.run(
                [
                    "scamper",
                    "-O",
                    "warts",
                    "-o",
                    self.storage.operation_filename_tmp(task),
                    "-c"
                ] + operation.params
            )

            self.communicator.finish_task(operation, task)

        self.communicator.finish_operation(operation)
