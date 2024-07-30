class Timeline:
    def __init__(self, total_time):
        """
        Initialize the timeline with total time for the schedule.

        Args:
            total_time (float): The total time for the schedule (hyperperiod).
        """

        self.current_time = 0.0
        self.total_time = total_time
        self.tasks = []



    def add_task(self,task, duration):
        """
        Add a task to the timeline for a given duration.

        Args:
            task (Task): The task to be added.
            duration (float): The duration for which the task will be executed.
        """

        fromtime = self.current_time
        endtime = fromtime + duration
        self.tasks.append([task.name, fromtime, endtime])
        self.current_time = endtime



    def info(self):
        """
        Get the current timeline information.

        Returns:
            str: A string representation of the current timeline and tasks.
        """

        return (f"TIMELINE: current time: {self.current_time}     tasks: {self.tasks}")
