from common.communicator import TASK_SENT, TASK_FINISHED, IN_PROCESS

class Operation:
    def __init__(self, id_, params, credits_, cron, times_per_minute, stop_time):
        self.id = id_
        self.params = params
        self.credits = credits_
        self.tasks = []
        self.status = IN_PROCESS,
        self.cron = cron,
        self.times_per_minute = times_per_minute,
        self.stop_time = stop_time
    
    def add_task(self, task):
        self.tasks.append(task)

    def update_task(self, a_task, status):
        for task in self.tasks:
            if task.code == a_task:
                task.status = status

    def all_task_sent(self):
        for task in self.tasks:
            if task.status != TASK_SENT:
                return False
        
        return True

    def finished_tasks(self):
        finished_tasks = []

        for task in self.tasks:
            if task.status == TASK_FINISHED:
                finished_tasks.append(task)
        
        return finished_tasks

    def data(self):
        return self.__dict__

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "Operation: " + str(self.data())

    def __str__(self):
        return "Operation: " + str(self.data())
