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

def main():
    if len(sys.argv) != 2:
        print("[USAGE:] python3 ece_652_final.py <workload_file.txt>")
        return

    file_name = sys.argv[1]
    print(f"file name is: {file_name}")

if __name__ == "__main__":
    main()
