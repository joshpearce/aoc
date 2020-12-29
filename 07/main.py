from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set
from collections import defaultdict

# modifying my solution more simple, inspired by:
# https://github.com/James-Ansley/adventofcode/blob/master/answers/day07.py

def parse_file(file_path: str) -> Tuple[Dict[str, List[Tuple[int, str]]], Dict[str, Set[str]]]:
    forward_edges: Dict[str, List[Tuple(int, str)]] = {}
    backward_edges: Dict[str, Set(str)] = defaultdict(set)
    with file_path.open("r") as file:
        for line in file.readlines():
            parts = line.split("bags contain")
            container_clr = parts[0].strip()
            forward_edges[container_clr] = []        
            rules = parts[1].split(",")
            for rule in rules:
                rule_parts = rule.strip().split(" ")
                if not rule_parts[0] == "no":
                    qnt = int(rule_parts[0])
                    containee_clr = " ".join(rule_parts[1:-1])
                    forward_edges[container_clr].append((containee_clr, qnt))
                    backward_edges[containee_clr].add(container_clr)
    return forward_edges, backward_edges



def run(file_path: Path) -> None:

    looking_for = "shiny gold"
    forward_edges, backward_edges = parse_file(file_path)

    bags = set(backward_edges[looking_for])
    results: Set[str] = set()
    while bags:
        bag = bags.pop()
        results.add(bag)
        bags |= backward_edges[bag]
    print(f'{len(results)} bags can eventually contain {looking_for}')

    containees = list(forward_edges[looking_for])
    count = 0
    while containees:
        containee = containees.pop()
        count += containee[1]
        containees += [ (color, containee[1] * x) for color, x in forward_edges[containee[0]] ]
    print(f'A {looking_for} bag can contain a total of {count} other bags')

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)