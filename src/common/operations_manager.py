from multiprocessing import Process, SimpleQueue
from common.operation import Operation

STOP = 0
NEW_DATA = 1

IN_PROCESS = 0
FINISHED = 1
SENT = 2

class OperationsManager():
    def __init__(self, storage):
        self.queue = SimpleQueue()
        self.storage = storage
        self.current_ops = self.storage.read_operations_state()

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
        
    def stop(self):
        self.queue.put(STOP)
        self.p.join()
        print("Operation manager stopped")

    def run(self):
        print("Running with: ", self.current_ops)

        while self.queue.get() != STOP:
            [operation_data, status] = self.queue.get()

            print(operation_data)

            operation = Operation(
                operation_data["id"],
                operation_data["params"]
            )

            if status == SENT:
                self.delete_operation(operation)
            else:
                self.current_ops[operation] = status

            self.save_current_status()

            print("Current ops after: ", self.current_ops)

        print("Operation manager ending its work...")

    def add_operation(self, operation):
        self.queue.put(NEW_DATA)
        self.queue.put([operation.data(), IN_PROCESS])

    def end_operation(self, operation):
        self.storage.mark_operation_finished(operation)
        self.queue.put(NEW_DATA)
        self.queue.put([operation.data(), FINISHED])

    def remove_operation(self, operation):
        self.queue.put(NEW_DATA)
        self.queue.put([operation.data(), SENT])

    def save_current_status(self):
        self.storage.save_operations_state(self.current_ops)

    def delete_operation(self, operation):
        self.storage.remove_operation(operation)
        del self.current_ops[operation]
