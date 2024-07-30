class Timeline:
    def __init__(self, total_time):
        self.currenttime = 0.0
        self.totaltime = 10000
        self.currenttask = total_time
        self.tasks = []


    def add_task(self,task, duration):
        fromtime = self.currenttime
        endtime = fromtime + 1
        self.tasks.append([task.id, fromtime, endtime])
        self.currenttime = endtime


    def info(self):
        return (f"TIMELINE: current time: {self.current_time}     tasks: {self.tasks}")
