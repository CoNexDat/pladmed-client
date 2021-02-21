from multiprocessing import Process, SimpleQueue

STOP = 0
NEW_DATA = 1

IN_PROCESS = 0
FINISHED = 1
SENT = 2

class OperationsManager():
    def __init__(self):
        self.current_ops = {}
        self.queue = SimpleQueue()
        # Remove possible dangling data deleted
    
    def start(self):
        self.p = Process(target=self.run)
        self.p.start()
        
    def stop(self):
        self.queue.put(STOP)
        self.p.join()
        print("Operation manager stopped")

    def run(self):
        while self.queue.get() != STOP:
            [operation, status] = self.queue.get()

            if status == SENT:
                del self.current_ops[operation]
            else:
                self.current_ops[operation] = status

            print("Current ops after: ", self.current_ops)

        print("Operation manager ending its work...")

    def add_operation(self, op_id):
        self.queue.put(NEW_DATA)
        self.queue.put([op_id, IN_PROCESS])

    def end_operation(self, op_id):
        self.queue.put(NEW_DATA)
        self.queue.put([op_id, FINISHED])

    def remove_operation(self, op_id):
        self.queue.put(NEW_DATA)
        self.queue.put([op_id, SENT])
