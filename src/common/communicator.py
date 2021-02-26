from multiprocessing import SimpleQueue

STOP = 0
NEW_DATA = 1

IN_PROCESS = 0
FINISHED = 1
TASK_FINISHED = 2
TASK_SENT = 3
CREDITS = 4

class Communicator:
    def __init__(self):
        self.transmit_queue = SimpleQueue()
        self.operations_queue = SimpleQueue()
        self.client_queue = SimpleQueue()
    
    def read_operations(self):
        return self.operations_queue.get()

    def add_operation(self, operation):
        self.operations_queue.put([
            NEW_DATA,
            IN_PROCESS,
            operation.data()
        ])

    def finish_operation(self, operation):
        self.operations_queue.put([
            NEW_DATA,
            FINISHED,
            operation.data()
        ])
    
    def finish_task(self, operation, task_code):
        self.operations_queue.put([
            NEW_DATA,
            TASK_FINISHED,
            operation.data(),
            task_code
        ])

    def sent_task(self, operation, task_code):
        self.operations_queue.put([
            NEW_DATA,
            TASK_SENT,
            operation.data(),
            task_code
        ])

    def stop_operations(self):
        self.operations_queue.put([STOP])

    def read_transmit(self):
        return self.transmit_queue.get()
    
    def stop_transmit(self):
        self.transmit_queue.put([STOP])

    def notify_end_task(self, operation, task_code):
        self.transmit_queue.put([
            NEW_DATA,
            operation.data(),
            task_code
        ])

    def get_current_credits(self):
        self.operations_queue.put([
            NEW_DATA,
            CREDITS
        ])

        return self.client_queue.get()

    def notify_current_credits(self, credits_):
        self.client_queue.put(
            credits_
        )
