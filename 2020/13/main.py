from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set


def run(file_path: Path) -> None:
    me, buses = file_path.read_text().strip().split('\n')
    me = int(me)
    buses = [int(b) for b in buses.split(',') if b != 'x']
    wait = lambda x: x - me % x
    waits = [wait(b) for b in buses]
    min_wait = min(waits)
    bus = buses[waits.index(min_wait)]
    print(min_wait * bus)


def part2(file_path: Path) -> None:
    buses = file_path.read_text().strip().split('\n')[1]
    buses = [(int(i), int(b))
              for i, b in enumerate(buses.split(',')) if b != 'x']

    time = 0
    step = 1

    for bus in buses:
        while True:
            if (time+bus[0]) % bus[1] == 0:
                step *= bus[1]
                break
            time += step

    print(time)

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)
    part2(file_path)
