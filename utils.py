import math
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

def lcm_float(a, b, precision=5):
    a = round(a, precision)
    b = round(b, precision)
    return LCM(int(a*10**precision), int(b*10**precision))/10**precision


def calculate_hyperperiod(task_list):
    r"""
    Calculate the hyperperiod of a set of tasks

    Args:
        task_list (list) - A list of tuple, each containing (execution_time, period, deadline) of a task

    Returns
        int: The hyperperiod of the task set.
    """

    # hyperperiod = int(task_list[0][1])
    hyperperiod = task_list[0][1]
    print(f"first hyper: {hyperperiod}")
    for _, task_period, _ in task_list[1:]:
        # hyperperiod = LCM(int(hyperperiod), int(task_period))
        print(f"task period: {task_period}")
        hyperperiod = lcm_float(hyperperiod, task_period)

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



# NOT USE
def is_schedulable_using_utilization(tasks):
    r"""
    Check if the task set is schedulable under the Deadline Monotonic algorithm using utilization.

    Args:
        tasks (list): List of Task objects

    Returns:
        bool: True if schedulable, False otherwise
    """

    utilization = sum(task.executiontime / min(task.deadline, task.period) for task in tasks)
    return utilization <= 1



from math import ceil
def calculate_response_time(task, higher_priority_tasks):
    """
    Calculate the worst-case response time for a task using response time analysis.

    Args:
        task (Task): The task for which to calculate the response time.
        higher_priority_tasks (list): List of higher priority Task objects.

    Returns:
        float: The worst-case response time for the task.


    Reference:
        The condition is reference from this slide: https://www.cse.wustl.edu/~lu/cse467s/slides/example_sched.pdf
    """

    R = task.executiontime
    while True:
        interference = sum(ceil(R / t.period) * t.executiontime for t in higher_priority_tasks)
        new_R = task.executiontime + interference
        if new_R == R:
            break
        if new_R > task.deadline:
            return float('inf')  # Task is not schedulable
        R = new_R
    return R



def is_schedulable(tasks):
    """
    Check if the task set is schedulable under the Deadline Monotonic algorithm using response time analysis.

    Args:
        tasks (list): List of Task objects.

    Returns:
        bool: True if schedulable, False otherwise.
    """

    tasks = order_by_deadline(tasks)
    for i, task in enumerate(tasks):
        higher_priority_tasks = tasks[:i]
        R = calculate_response_time(task, higher_priority_tasks)
        if R > task.deadline:

            return False

    return True



# NOT USE
def is_schedulable_using_response_time(tasks):
    r"""
    Check if the task set is schedulable under the Deadline Monotonic algorithm using response time analysis.

    Args:
        tasks (list): List of Task objects

    Returns:
        bool: True if schedulable, False otherwise
    """

    for i, task in enumerate(tasks):
        R = task.executiontime
        while True:
            R_next = task.executiontime + sum(
                (R / tasks[j].period) * tasks[j].executiontime
                for j in range(i)
            )
            if R_next == R:
                break
            R = R_next
        if R > task.deadline:

            return False

    return True



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
                expected_executing_task.preemptions += 1


        return ordered_by_priority[0]
    else:

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

        # Task added time equal to its execution time (finish executing)
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
