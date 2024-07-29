class Task:
    def __init__(self, id, executiontime, period, deadline):
        self.id = id
        self.executiontime = executiontime
        self.period = period
        self.deadline = deadline
        self.next_available = 0
        self.executed = False
        self.addedtime = 0      # This is time already executed from current period
