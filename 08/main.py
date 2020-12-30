from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set, ByteString
from struct import pack, unpack
from time import sleep

def get_program_data(file_path: Path) -> ByteString:
    prog: ByteString = bytearray()
    with file_path.open("r") as file:
        prog = [ l.split(" ") for l in file.readlines()]
        prog = [pack('3sh', bytes(op, 'ascii'), int(operand) ) for op, operand in prog]
        prog_joined = bytearray(b''.join(prog))

        return prog_joined

def run_prog(prog: ByteString) -> str:
    pc, width, acc = 0, 6, 0
    count = len(prog) / width
    while pc < count:
        op, d = unpack('3sh', prog[pc*width:pc*width+width])
        prog[pc*width:pc*width+width] = pack('3sh', b'---', 0)
        if op == b'nop':
            pc += 1
        elif op == b'acc':
            acc += d
            pc += 1
        elif op == b'jmp':
            pc += d
        elif op == b'---':
            return f'Program in loop. Acc is {acc}.'
        #print(f'  pc: {pc}')
    
    return f'Program terminated normally. Acc is {acc}'

def run(file_path: Path) -> None:
    prog = get_program_data(file_path)

    prog_copy = bytearray(prog)
    print(run_prog(prog_copy))

    pc, width = 0, 6
    count = len(prog) / width
    while pc < count:
        prog_copy = bytearray(prog)

        op, d = unpack('3sh', prog_copy[pc*width:pc*width+width])
        if op == b'nop':
            prog_copy[pc*width:pc*width+width] = pack('3sh', b'jmp', d)
        elif op == b'jmp':
            prog_copy[pc*width:pc*width+width] = pack('3sh', b'nop', d)
        else:
            pc += 1
            continue

        result = run_prog(prog_copy)
        print(result)
        pc += 1
        if "normally" in result:
            return

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)