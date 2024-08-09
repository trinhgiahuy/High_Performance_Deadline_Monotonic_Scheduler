import math
from math import gcd
from timeline_class import Timeline
import time

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

def lcm_float(a, b, precision=3):
   # a = round(a, precision)
   # b = round(b, precision)
   # return LCM(int(a*10**precision), int(b*10**precision))/10**precision
    scale = 10 ** precision
    a_scaled = int(a * scale)
    b_scaled = int(b * scale)
    lcm_scaled = LCM(a_scaled, b_scaled)

    return lcm_scaled / scale

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
    print(f"[{current_time}]------------ Available tasks at time {current_time}: {[task.getName() for task in available]}")  # Debug

    if available:

        # List of tasks sorted based on deadline
        ordered_by_priority = order_by_deadline(available)
        print(f"[DEBUG] Ordered tasks by priority: {[task.getName() for task in ordered_by_priority]}")  # Debug

        # Preemption is considered from 2nd time unit run
        if not first_run:
            # print(f"[EVALUATE]: expected_executing_task {expected_executing_task.getName()} with expected_run: {expected_executing_task.getExpectedContinue()}")

            # Check last executed task if it is still expected to run in next evaluation
            # and it is not finish directly before the next available task with higer priority is available again (finish just-in-time)
            # and the next higher priority task retrieved is different from it
            if expected_executing_task.getExpectedContinue() \
            and expected_executing_task.getAddedTime() != expected_executing_task.getExecutionTime() \
            and ordered_by_priority[0].getName() != expected_executing_task.getName():
                print(f"[DEBUG] PREEMPTION HAPPEN HERE at current time {current_time}")  # Debug
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
    # print(f"[get_next_event_time]current time {current_time}: tasks: {tasks}")
    next_times = [task.next_available for task in tasks if task.next_available > current_time]
    next_times.extend([round(task.next_available + task.period,3) for task in tasks if task.addedtime < task.executiontime])


    # Remove any times that are less than or equal to the current time
    # next_times = [time for time in next_times if time > current_time]

    print(f"[DEBUG] Next event times: {next_times}")  # Debug

    if next_times:
        next_event_time = min(next_times)
        # QUEST: Shall we remove the next_event_time from the list??
        next_times = [time for time in next_times if time != next_event_time]
        # next_event_index = next_times.index(next_event_time)
        # next_times.pop(next_event_index)  # Remove the next event time from the list
        print(f"[DEBUG] Next event time: {next_event_time}")  # Debug
        print(f"[DEBUG] Next event times after remove: {next_times}")  # Debug

        return round(next_event_time,3)

    return round(current_time + 1,3)



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
    print(f"[DEBUG] total_time: {total_time}")  # Debug
    timeline = Timeline(total_time)
    current_task = None

    first_run = True
    last_event_time = None
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
            print(f"[DEBUG] Idle time from {timeline.current_time} to {next_event_time}")  # Debug
            timeline.tasks.append(["  ", timeline.current_time, next_event_time])
            timeline.current_time = next_event_time
            continue


        # Handle the case where the execution time is not necessarily possitive integers with precision up to 0.001
        remaining_time = round(task.executiontime - task.addedtime, 3)
        next_event_time = get_next_event_time(tasks, timeline.current_time)

        if next_event_time == last_event_time:
            print("NO CHANGE FROM LAST")
        else:
            duration = min(remaining_time, round(next_event_time - timeline.current_time,3))
        print(f"[remaining_time {remaining_time}], next_event_time:{next_event_time}, timeline.current_time: {timeline.current_time}")
        print(f"get min {duration}")
        # Ensure we have positive duration
        if duration <= 0:
            print(f"[DEBUG] Non-positive duration detected. Current Time: {timeline.current_time}, Task: {task.name}, Duration: {duration}")
            break

        # DEBUG output
        print(f"[DEBUG] Scheduling Task: {task.name}")
        print(f"[DEBUG] Current Time: {timeline.current_time}, Task Duration: {duration}, Remaining Time: {remaining_time}, Next Event Time: {next_event_time}")


        timeline.add_task(task, duration)
        task.addedtime = round(task.addedtime + duration, 3)
        print(f"timeline info: {timeline.info()}")
        print(f"task info {task.info()}")

        # Continue add task to the timeline
        if task.addedtime < task.executiontime:
            print(f"[*] Add task to timeline")
            task.expected_continue = True

        # Task added time equal to its execution time (finish executing)
        # Reset parameter, prepare to switch to another task
        else:
            print(f"[*] Task = exec time")
            task.addedtime = 0.0
            task.completed = True
            task.expected_continue = False
            task.next_available = round(task.next_available + task.period,3)
            # task.next_available = timeline.current_time + task.period
            print(f"task info {task.info()}")

        # timeline.current_time = round(timeline.current_time + duration, 3)  # Ensure current_time advances
        timeline.current_time = round(timeline.current_time, 3)
        if task is not None:
            current_task = task
            expected_task_first_run = task

        # Avoid infinite loop
        if timeline.current_time >= total_time:
            print("AVOID INFINITELOOP")
            break

        last_event_time = next_event_time
        # time.sleep(1)
    return timeline, tasks
