#!/bin/bash

reference_file="expected_results_652.txt"

total_cases=0
pass_cases=0
fail_cases=0

read_expected_results() {
    local workload=$1
    awk -v workload="$workload" '
    BEGIN { found=0 }
    $1 == "Workload" && $2 == workload":" { found=1; next }
    found && $1 == "Workload" { exit }
    found { print }
    ' "$reference_file"
}

for workload_file in workload1.txt workload2.txt workload3.txt workload4.txt workload5.txt workload6.txt; do
    workload_number=$(echo $workload_file | grep -o '[0-9]')
    echo "Workload $workload_number:"

    output=$(python3 ece_652_final.py "$workload_file")

    expected_output=$(read_expected_results "$workload_number")

    if [ "$output" == "$expected_output" ]; then
        echo "Pass"
        pass_cases=$((pass_cases + 1))
    else
        echo "Fail"
        echo "Expected:"
        echo "$expected_output"
        echo "Got:"
        echo "$output"
        fail_cases=$((fail_cases + 1))
    fi

    total_cases=$((total_cases + 1))
done

pass_percentage=$(echo "scale=2; ($pass_cases / $total_cases) * 100" | bc)
echo "Summary:"
echo "Total cases: $total_cases"
echo "Pass cases: $pass_cases"
echo "Fail cases: $fail_cases"
echo "Pass percentage: $pass_percentage%"
