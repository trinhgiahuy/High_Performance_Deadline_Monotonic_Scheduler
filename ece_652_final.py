# =============================================================================
#
# Script Name:
# Description:
# Author:
# Emai:
# Date:
# Usage:
#
#
# =============================================================================


import argparse
import sys

def main():
    if len(sys.argv) != 2:
        print("[USAGE:] python3 ece_652_final.py workload_test_file")
        return

    file_name = sys.argv[1]
    print(f"file name is: {file_name}")

if __name__ == "__main__":
    main()
