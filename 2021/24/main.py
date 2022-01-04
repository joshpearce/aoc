#!/usr/bin/env python3

from enum import Enum
from typing import List
import re
import threading
import numpy

# the program repeats the same instructions 14 times, but with slightly different constants.
# this regex returns arrays of the constants.
def parse_program_constants(program_test):
    results = re.findall(r'inp w\nmul x ([\-0-9]+)\nadd x z\nmod x ([\-0-9]+)\ndiv z ([\-0-9]+)\nadd x ([\-0-9]+)\neql x w\neql x 0\nmul y 0\nadd y ([\-0-9]+)\nmul y x\nadd y ([\-0-9]+)\nmul z y\nmul y 0\nadd y w\nadd y ([\-0-9]+)\nmul y x\nadd z y', program_test)
    numeric_constants = [list(map(int, groups)) for groups in results]
    return numeric_constants

# print(numpy.array(numeric_constants))
# [[  0  26   1  14  25   1  12]
#  [  0  26   1  10  25   1   9]
#  [  0  26   1  13  25   1   8]
#  [  0  26  26  -8  25   1   3]
#  [  0  26   1  11  25   1   0]
#  [  0  26   1  11  25   1  11]
#  [  0  26   1  14  25   1  10]
#  [  0  26  26 -11  25   1  13]
#  [  0  26   1  14  25   1   3]
#  [  0  26  26  -1  25   1  10]
#  [  0  26  26  -8  25   1  10]
#  [  0  26  26  -5  25   1  14]
#  [  0  26  26 -16  25   1   6]
#  [  0  26  26  -6  25   1   5]]


class ALU:

    def __init__(self, w=0, x=0, y=0, z=0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def to_tuple(self):
        return (self.w, self.x, self.y, self.z)

    def run_instruction(self, inst: str, a: str, b: str):
        a_ = getattr(self, a)
        b_ = getattr(self, b) if hasattr(self, b) else int(b)
        match inst:
            case "inp":
                a_ = b_
            case "add":
                a_ = a_ + b_
            case "mul":
                a_ = a_ * b_
            case "div":
                a_ =  a_ // b_
            case "mod":
                a_ = a_ % b_
            case "eql":
                a_ = int(a_ == b_)
        setattr(self, a, a_)

def run_program(alu: ALU, instructions: List[List[str]], model_num: int):
    
    model_num_str = list(reversed(str(model_num)))

    for inst in instructions:
        inst_copy = [x for x in inst]
        if inst_copy[0] == "inp":
            inst_copy.append(model_num_str.pop())    
        alu.run_instruction(inst_copy[0], inst_copy[1], inst_copy[2])
    
    return alu

def run_concice_loop(alu: ALU, digit: int, constants: List[int]) -> ALU:
    c = constants
    alu.w = digit
    alu.x = alu.z % 26
    alu.x = int((alu.x + c[3]) != alu.w)
    alu.y = 25 * alu.x + 1
    alu.z = alu.z // c[2]
    alu.z = alu.z * alu.y
    alu.y = (alu.w + c[6]) * alu.x
    alu.z = alu.z + alu.y

    return alu

def run_program2(model_num, constants):
    if "0" not in model_num:
        alu = ALU()
        for i in range(14):
            run_concice_loop(alu, int(model_num[i]), constants[i])
        return alu.z

def solve_range(start, end, constants):
    answers = []
    for i in range(start, end, -1):
        z = run_program2(str(i), constants)
        if z == 0:
            answers.append(i)
        if i % 100000 == 0:
            pct = ((start - i) / (start - end)) * 100
            print(f"milepost: {i}. answers: {answers}. % done: {pct:.5f}")


if __name__ == "__main__":

    from pathlib import Path

    program_test = (Path(__file__).parent / "input.txt").open().read()
    constants = parse_program_constants(program_test)
    lines = program_test.split("\n")
    instructions = [l.split(' ') for l in lines]

    print(run_program2("99999999999999", constants))

    #solve_range(99999999999999, 90000000000000, constants)
    
    # start = 99999999999999
    # step =  10000000000000
    # threads = []
    # for j in range(9):
    #     #print(f"{start-(j*step)} - {start-((j+1)*step)+1}")
    #     thread = threading.Thread(target=solve_range, args=(start-(j*step), start-((j+1)*step)+1, constants))
    #     threads.append(thread)
    #     thread.start()

    # for thread in threads:
    #     thread.join()