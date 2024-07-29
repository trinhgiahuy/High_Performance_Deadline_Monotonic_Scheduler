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
from math import gcd


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

    hyperperiod = task_list[0][1]
    for _, task_period, _ in task_list[1:]:
        hyperperiod = LCM(hyperperiod, task_period)

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
                task_execution_time, task_period, task_deadline = map(int, line.strip().split(','))
                print(f"{task_execution_time}, {task_period} {task_deadline}")
                task_list.append((task_execution_time, task_period, task_deadline))

    print(task_list)
    return task_list



def main():
    r"""
    Main fuction to execute the Deadline Monotonic scheduling simulator.
    """
    if len(sys.argv) != 2:
        print("[USAGE:] python3 ece_652_final.py <workload_file.txt>")
        return

    fileName = sys.argv[1]
    print(f"file name is: {fileName}")

    # Get the list of tasks from the input file
    task_list = get_tasks(fileName)

    # Cacluate the hyperperiod of task set
    hyperperiod = calculate_hyperperiod(task_list)
    print(hyperperiod)






if __name__ == "__main__":
    main()
