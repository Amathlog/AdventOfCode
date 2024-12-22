import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.multithread import execute_async

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def prune(v :int) -> int:
    return v % 16777216

def mix(v1: int, v2: int) -> int:
    return v1 ^ v2

def apply(v: int, shift: int) -> int:
    if shift < 0:
        return prune(mix(v, v >> abs(shift)))
    else:
        return prune(mix(v, v << shift))

def next_secret(v: int) -> int:
    v = apply(v, 6)
    v = apply(v, -5)
    return apply(v, 11)

@profile
def part_one(entry: List[str]) -> int:
    count = 0
    for e in entry:
        v = int(e)
        for _ in range(2000):
            v = next_secret(v)
        count += v

    return count

@profile
def solve(entry: List[str]) -> int:
    prices = []
    differences = []
    seq_values = []
    all_possible_sequences = set()
    count = 0

    for e in entry:
        v = int(e)
        prices.append([v % 10])
        differences.append([])
        seq_values.append({})
        for _ in range(2000):
            v = next_secret(v)
            prices[-1].append(v % 10)
            differences[-1].append(prices[-1][-1] - prices[-1][-2])
            if len(differences[-1]) >= 4:
                seq = (differences[-1][-4], differences[-1][-3], differences[-1][-2], differences[-1][-1])
                all_possible_sequences.add(seq)
                if seq not in seq_values[-1]:
                    seq_values[-1][seq] = prices[-1][-1]
        count += v

    max = -1
    best_seq = None
    for seq in all_possible_sequences:
        sum_price = 0
        for seq_value in seq_values:
            if seq in seq_value:
                sum_price += seq_value[seq]
        
        if sum_price > max:
            max = sum_price
            best_seq = seq

    return count, best_seq, max

def compute_secret(v: int) -> List[int]:
    prices = [v % 10]
    differences = []
    seq_values = {}
    for _ in range(2000):
        v = next_secret(v)
        prices.append(v % 10)
        differences.append(prices[-1] - prices[-2])
        if len(differences) >= 4:
            seq = (differences[-4], differences[-3], differences[-2], differences[-1])
            if seq not in seq_values:
                seq_values[seq] = prices[-1]
    
    return seq_values, v

seq_values = {}

def compute_all_sequences(seq: Tuple[int,int,int,int]) -> int:
    global seq_values
    sum_price = 0
    for seq_value in seq_values:
        if seq in seq_value:
            sum_price += seq_value[seq]
    return sum_price

@profile
def solve_multithread(entry: List[str]) -> int:
    global seq_values
    nb_threads = 16
    seq_values, final_secrets = zip(*execute_async(nb_threads, compute_secret, [int(e) for e in entry]))

    all_possible_sequences = set()
    for seq_value in seq_values:
        all_possible_sequences.update(seq_value.keys())

    return sum(final_secrets), execute_async(nb_threads, compute_all_sequences, all_possible_sequences, max)


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve_multithread(example_entries))
    print("Part 1 and 2 entry:", solve_multithread(entries))
