import random
from sympy.ntheory import isprime

def generate_prime(bits: int) -> int:
    while True:
        candidate = random.randint(2 ** bits, 2 ** (bits+1) - 1)
        if isprime(candidate):
            return candidate

def generate_large_workload(n: int, exectime_bits: int, period_bits: int):
    """Mostly a performance test, pick small exectime_bits so the workload is likely to be feasible
    """
    workload = [(generate_prime(exectime_bits), generate_prime(period_bits)) for _ in range(n)]
    for (exectime, period) in workload:
        print(f"{exectime},{period},{period}")
 