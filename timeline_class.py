class Timeline:
    def __init__(self, total_time):
        self.current_time = 0.0
        self.total_time = total_time
        self.tasks = []


    def add_task(self,task, duration):
        fromtime = self.current_time
        endtime = fromtime + duration
        self.tasks.append([task.name, fromtime, endtime])
        self.current_time = endtime


    def info(self):
        return (f"TIMELINE: current time: {self.current_time}     tasks: {self.tasks}")
