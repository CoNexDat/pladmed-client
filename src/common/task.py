from common.communicator import TASK_FINISHED

class Task:
    def __init__(self, code):
        self.code = code
        self.status = TASK_FINISHED
    
    def data(self):
        return self.__dict__

    def __eq__(self, other):
        return self.code == other.code

    def __repr__(self):
        return "Task: " + str(self.code) + " " + str(self.status)

    def __str__(self):
        return "Task: " + str(self.code) + " " + str(self.status)
