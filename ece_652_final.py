# =============================================================================
#
# Script Name:      ece_657_final.py
# Description:      This script will implements a simulator for the Deadline Monotonic
#                   scheduling algorithm on a single-core CPU. It reads a set of
#                   periodic tasks from a file, determines if the task set is
#                   schedulable under the Deadline Monotonic algorithm, and reports
#                   the number of times each task is preempted per hyperperiod.
# Author:           Huy Trinh
# Emai:             h3trinh@uwaterloo.ca
# Date:             28 Jul, 2024
# Usage:
#               python3 ece_621_final.py <worload_file.txt>
#
# =============================================================================


import argparse
import sys
from task_class import Task
# from timeline_class import Timeline
from utils import *





def main():
    r"""
    Main fuction to execute the Deadline Monotonic scheduling simulator.
    """
    if len(sys.argv) != 2:
        print("[USAGE:] python3 ece_652_final.py <workload_file.txt>")
        return

    fileName = sys.argv[1]

    # Get the list of tasks from the input file
    task_list = get_tasks(fileName)

    # Cacluate the hyperperiod of task set
    hyperperiod = calculate_hyperperiod(task_list)


    tasks = [Task(f"T{i}", execution_time, period, deadline) for i, (execution_time, period, deadline) in enumerate(task_list)]

    if is_schedulable(tasks):
        expected_task_first_run = get_first_task_run(tasks)
        timeline, tasks = schedule(tasks, hyperperiod, expected_task_first_run)
        print(1)
        print_preemptions(tasks)
    else:
        print(0)



if __name__ == "__main__":
    main()
