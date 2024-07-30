#!/bin/bash

REFERENCE_FILE="expected_results_652.txt"
WORKLOAD_FILES=("workload1.txt" "workload2.txt" "workload3.txt" "workload4.txt" "workload5.txt" "workload6.txt")

PROGRAM="python3 ece_652_final.py"

total_cases=0
pass_cases=0
fail_cases=0

mapfile -t reference < "$REFERENCE_FILE"

for i in "${!WORKLOAD_FILES[@]}"; do
    workload="${WORKLOAD_FILES[$i]}"
    
    ref_output=()
    ref_index=$((i * 3))
    ref_output+=("${reference[ref_index + 1]}")
    ref_output+=("${reference[ref_index + 2]}")

    output=($($PROGRAM "$workload"))

    if [[ "${ref_output[@]}" == "${output[@]}" ]]; then
        ((pass_cases++))
        echo "Workload $((i+1)): Pass"
    else
        ((fail_cases++))
        echo "Workload $((i+1)): Fail"
        echo "Expected:"
        printf "%s\n" "${ref_output[@]}"
        echo "Got:"
        printf "%s\n" "${output[@]}"
    fi
    ((total_cases++))
done

pass_percentage=$((100 * pass_cases / total_cases))

echo "Summary:"
echo "Total cases: $total_cases"
echo "Pass cases: $pass_cases"
echo "Fail cases: $fail_cases"
echo "Pass percentage: $pass_percentage%"

