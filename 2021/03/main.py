#!/usr/bin/env python3

from os import error
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from typing import Iterator
from contextlib import suppress
from utils import advent
from functools import reduce


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    matrix = advent.read_num_array_from_file(file_path)
    length = len(matrix)

    # part 1
    sums = [sum(l) for l in zip(*matrix)]
    gamma = [1 if i/length >= 0.5 else 0 for i in sums]
    gamma_num = reduce(lambda a, b: (a << 1) + b, gamma)
    print(f"gamma: {gamma_num}")

    for c in gamma:
        if c != 0 and length / c == 2:
            raise ValueError("Ambiguous input")
    
    epsilon = [0 if i else 1 for i in gamma]
    epsilon_num = reduce(lambda a, b: (a << 1) + b, epsilon)
    print(f"epsilon: {epsilon_num}")
    
    print(f"power consumption: {gamma_num * epsilon_num}")

    # part 2

    # deep copy data
    most_common = list(gamma)
    least_commom = list(epsilon)
    oxygen_rating = [row[:] for row in matrix]
    scrubber_rating = [row[:] for row in matrix]

    # oxygen rating
    for i in range(len(oxygen_rating[0])):
        oxygen_rating = list(filter(lambda r: r[i] == most_common[i], oxygen_rating))
        if len(oxygen_rating) == 1:
            break
        sums = [sum(l) for l in zip(*oxygen_rating)]
        most_common = [1 if i/len(oxygen_rating) >= 0.5 else 0 for i in sums]
    
    oxygen_rating_num = reduce(lambda a, b: (a << 1) + b, oxygen_rating[0])
    print(f"oxygen rating: {oxygen_rating_num}")

    # scrubber rating
    for i in range(len(scrubber_rating[0])):
        scrubber_rating = list(filter(lambda r: r[i] == least_commom[i], scrubber_rating))
        if len(scrubber_rating) == 1:
            break
        sums = [sum(l) for l in zip(*scrubber_rating)]
        least_commom = [1 if i/len(scrubber_rating) < 0.5 else 0 for i in sums]
    
    scrubber_rating_num = reduce(lambda a, b: (a << 1) + b, scrubber_rating[0])
    print(f"oxygen rating: {scrubber_rating_num}")

    print(f"life support rating: {oxygen_rating_num * scrubber_rating_num}")





        

