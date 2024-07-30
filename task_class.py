class Task:
    def __init__(self, name, executiontime, period, deadline):
        """
        Initialize a task with its attributes.

        Args:
            name (str): The name of the task.
            executiontime (float): The execution time of the task.
            period (float): The period of the task.
            deadline (float): The deadline of the task.
        """

        self.period = period
        self.executiontime = executiontime
        self.deadline = deadline
        self.next_available = 0
        self.name = name
        self.completed = False      # Completed of the task within each of its period
        self.addedtime = 0.0        # Already executed time in the current period
        self.preemptions = 0        # Track number of preemptions
        self. expected_continue = False



    def info(self):
        """
        Get the information of the task.

        Returns:
            str: A string representation of the task's current state.
        """

        return (f"{self.name}, exectime {self.executiontime} next_avai:{self.next_available} executed:{self.completed} addedtime:{self.addedtime} expected_continue: {self.expected_continue} preemptions:{self.preemptions}")



    def getName(self):
        """
        Get the name of the task.

        Returns:
            str: The name of the task.
        """

        return f"{self.name}"



    def getExpectedContinue(self):
        """
        Get the expected continue status of the task.

        Returns:
            bool: True if the task is expected to continue, False otherwise.
        """

        return self.expected_continue



    def getAddedTime(self):

        """
        Get the added time (executed time) of the task.

        Returns:
            float: The added time of the task.
        """

        return self.addedtime



    def getExecutionTime(self):
        """
        Get the execution time of the task.

        Returns:
            float: The execution time of the task.
        """

        return self.executiontime
