class Task:
    def __init__(self, name, period, executiontime, deadline):
        self.period = period
        self.executiontime = executiontime
        self.deadline = deadline
        self.next_available = 0.0
        self.name = name
        self.completed = False      # Completed of the task within each of its period
        self.addedtime = 0.0        # Already executed time in the current period
        self.preemptions = 0        # Track number of preemptions
        self. expected_continue = False

    def info(self):
        return (f"{self.name}, exectime {self.executiontime} next_avai:{self.next_available} executed:{self.completed} addedtime:{self.addedtime} expected_continue: {self.expected_continue} preemptions:{self.preemptions}")


    def getName(self):
        return f"{self.name}"


    def getExpectedContinue(self):
        return self.expected_continue


    def getAddedTime(self):
        return self.executiontime

