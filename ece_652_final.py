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

def get_tasks(filename):

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
    if len(sys.argv) != 2:
        print("[USAGE:] python3 ece_652_final.py <workload_file.txt>")
        return

    fileName = sys.argv[1]
    print(f"file name is: {fileName}")

    task_list = get_tasks(fileName)

if __name__ == "__main__":
    main()
