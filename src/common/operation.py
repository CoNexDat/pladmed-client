class Operation:
    def __init__(self, id_, params, cron, times_per_minute, stop_time):
        self.id = id_
        self.params = params
        self.cron = cron
        self.times_per_minute = times_per_minute
        self.stop_time = stop_time
    
    def data(self):
        return self.__dict__

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "Operation: " + str(self.id)

    def __str__(self):
        return "Operation: " + str(self.id)
