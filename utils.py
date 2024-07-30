from math import gcd
from timeline_class import Timeline

def LCM(a,b):
    r"""
    Calculate the Least Common Multiplier (LCM) between two integers.


    Args:
        a (int) - first integer number
        b (int) - sencond integer number

    Returns:
        int: The LCM of the two integer
    """

    return abs(a*b) // gcd(a,b)



def calculate_hyperperiod(task_list):
    r"""
    Calculate the hyperperiod of a set of tasks

    Args:
        task_list (list) - A list of tuple, each containing (execution_time, period, deadline) of a task

    Returns
        int: The hyperperiod of the task set.
    """

    hyperperiod = int(task_list[0][1])
    for _, task_period, _ in task_list[1:]:
        hyperperiod = LCM(int(hyperperiod), int(task_period))

    return hyperperiod



def get_tasks(filename):
    r"""
    Read a file containing task definition and return a list of tasks.


    Args:
        filename(str) - The name of the file containing the tasks

    Returns:
        list: A list of tuples, each containing (execution_time, period, deadline) of a task
    """

    task_list = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                task_execution_time, task_period, task_deadline = map(float, line.strip().split(','))
                task_list.append((task_execution_time, task_period, task_deadline))

    return task_list



def is_schedulable(tasks):
    r"""
    Check if the task set is schedulable under the Deadline Monotonic algorithm.

    Args:
        tasks (list): List of Task objects

    Returns:
        bool: True if schedulable, False otherwise
    """

    utilization = sum(task.executiontime / min(task.deadline, task.period) for task in tasks)
    return utilization <= 1



def get_first_task_run(tasks):
    r"""
    Get the first task to run based on the earliest deadline.

    Args:
        tasks (list): List of Task objects

    Returns:
        Task: The first task to run
    """
    tmp_list = order_by_deadline(tasks)
    return tmp_list[0]



def order_by_deadline(tasks):
    r"""
    Order the tasks by their deadlines in ascending order.

    Args:
        tasks (list): List of Task objects

    Returns:
        list: List of Task objects ordered by deadlines
    """

    tasks.sort(key=lambda x: x.deadline)
    return tasks


def available_tasks(tasks, current_time):
    """
    Get the list of tasks that are available at the current time.

    Args:
        tasks (list): List of Task objects
        current_time (float): The current time in the timeline

    Returns:
        list: List of available Task objects
    """

    return [task for task in tasks if current_time >= task.next_available]


def preempted(tasks, current_time, expected_executing_task, first_run):
    """
    Determine if a task should be preempted by sorting based on the ordered of tasks' deadline
    If no task is found(Idle time), it returns None

    Args:
        tasks (list): List of Task objects
        current_time (float): The current time in the timeline
        expected_executing_task (Task): The task expected to continue execution
        first_run (bool): Flag indicating if it's the first run

    Returns:
        Task: The next task to be executed
    """

    # Retrieve all available tasks by time
    available = available_tasks(tasks, current_time)

    if available:

        # List of tasks sorted based on deadline
        ordered_by_priority = order_by_deadline(available)

        # Preemption is considered from 2nd time unit run
        if not first_run:
            # print(f"[EVALUATE]: expected_executing_task {expected_executing_task.getName()} with expected_run: {expected_executing_task.getExpectedContinue()}")

            # Check last executed task if it is still expected to run in next evaluation
            # and it is not finish directly before the next available task with higer priority is available again (finish just-in-time)
            # and the next higher priority task retrieved is different from it
            if expected_executing_task.getExpectedContinue() \
            and expected_executing_task.getAddedTime() != expected_executing_task.getExecutionTime() \
            and ordered_by_priority[0].getName() != expected_executing_task.getName():
                #print("Preemption should take place here")
                #print(f"{expected_executing_task.getName()} got preempted")
                expected_executing_task.preemptions += 1
            # elif expected_executing_task.getAddedTime() == expected_executing_task.getExecutionTime():
            #    print("**************************** ALREADY ADDED TO TIMELINE. RESET AND PREPARE TO TRANS NEXT ITER")
            # else:
            #    print("**************************RUN NORMAL")

            #print(f"[EVALUATE]: expected_executing_task {expected_executing_task.getName()} with expected_run: {expected_executing_task.getExpectedContinue()}")
            #if expected_executing_task.getExpectedContinue() == True:
            #    finish_before_trans = (expected_executing_task.getAddedTime() == expected_executing_task.getExecutionTime())
            #
            #    if not finish_before_trans and (ordered_by_priority[0].getName() != expected_executing_task.getName()):
            #        print("**************************PREEMPT HAPPENS!!")
            #        print(f"{expected_executing_task.getName()} got preempted")
            #        expected_executing_task.preemptions += 1
            #    elif finish_before_trans:
            #        print("**************************** ALREADY ADDED TO TIMELINE. RESET AND PREPARE TO TRANS NEXT ITER")
            #    else:
            #        print("**************************RUN NORMAL")
            #else:
            #    print(f"******************TRANS TO OTHER TASK")

        return ordered_by_priority[0]
    else:
        # print("Other cases")
        return None



def get_next_event_time(tasks, current_time):
    """
    Get the next event time for the tasks.

    Args:
        tasks (list): List of Task objects
        current_time (float): The current time in the timeline

    Returns:
        float: The next event time
    """

    next_times = [task.next_available for task in tasks if task.next_available > current_time]
    next_times.extend([task.next_available + task.period for task in tasks if task.addedtime < task.executiontime])

    if next_times:
        return min(next_times)

    return current_time + 1


def print_preemptions(tasks):
    """
    Print the number of preemptions for each task.

    Args:
        tasks (list): List of Task objects
    """
    tasks.sort(key=lambda x: x.name)
    preemptions = [task.preemptions for task in tasks]

    print(",".join(map(str, preemptions)))




def schedule(tasks, total_time, expected_task_first_run):
    """
    Main fucntion to schedule the tasks based on the Deadline Monotonic algorithm.

    Args:
        tasks (list): List of Task objects
        total_time (float): The total time for the schedule (hyperperiod)
        expected_task_first_run (Task): The task expected to run first

    Returns:
        Timeline, list: The timeline and the updated list of tasks
    """
    timeline = Timeline(total_time)
    current_task = None
    first_run = True

    # Main flow cotrol the logic of DM algorithm
    while timeline.current_time < timeline.total_time:
        if first_run:
            task = preempted(tasks, timeline.current_time, expected_task_first_run, True)
            first_run = False
        else:
            task = preempted(tasks, timeline.current_time, expected_task_first_run, False)


        # Schedlule the idle time units
        if task is None:
            next_event_time = get_next_event_time(tasks, timeline.current_time)
            timeline.tasks.append(["  ", timeline.current_time, next_event_time])
            timeline.current_time = next_event_time
            continue


        # Handle the case where the execution time is not necessarily possitive integers with precision up to 0.001
        remaining_time = task.executiontime - task.addedtime
        next_event_time = get_next_event_time(tasks, timeline.current_time)
        duration = min(remaining_time, next_event_time - timeline.current_time)

        timeline.add_task(task, duration)
        task.addedtime += duration

        # Continue add task to the timeline
        if task.addedtime < task.executiontime:
            task.expected_continue = True

        # Task added time equal to its execution time
        # Reset parameter, prepare to switch to another task
        else:
            task.addedtime = 0.0
            task.completed = True
            task.expected_continue = False
            task.next_available += task.period

        if task is not None:
            current_task = task
            expected_task_first_run = task


    return timeline, tasks
