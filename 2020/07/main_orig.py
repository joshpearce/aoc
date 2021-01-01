from __future__ import annotations
from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set
import copy

def parse_file(file_path: Path) -> Tuple[Set[str], Set[Tuple[str, str, int]]]:
    colors: Set[str] = set()
    all_rules: Set[Tuple[str, str, int]] = set()
    with file_path.open("r") as file:
        for line in file.readlines():
            parts = line.split("bags contain")
            bag_clr = parts[0].strip()
            colors.add(bag_clr)        
            rules = parts[1].split(",")
            for rule in rules:
                rule_parts = rule.strip().split(" ")
                if not rule_parts[0] == "no":
                    qnt = int(rule_parts[0])
                    rule_bag_clr = " ".join(rule_parts[1:-1])
                    all_rules.add((bag_clr, rule_bag_clr, qnt))
    return colors, all_rules

def can_eventually_contain(src: str, dst: str, rules: Set[Tuple[str, str, int]], visited: List[str]) -> bool:
    for rule in rules:
        if rule[0] == src:
            if rule[1] == dst:
                return True
            else:
                if rule[1] not in visited:
                    visited_copy = copy.deepcopy(visited)
                    visited_copy.append(src)
                    if can_eventually_contain(rule[1], dst, rules, visited_copy):
                        return True
    return False

def required_to_contain(src: str, rules: Set[Tuple[str, str, int]], visited: List[str]) -> int:
    count = 0
    for rule in rules:
        if rule[0] == src:
            count += rule[2]
            visited_copy = copy.deepcopy(visited)
            visited_copy.append(src)
            count += rule[2] * required_to_contain(rule[1], rules, visited)
    return count

def run(file_path: Path) -> None:

    looking_for = "shiny gold"
    colors, rules = parse_file(file_path)
    results = 0
    for clr in colors:
        if can_eventually_contain(clr, looking_for, rules, []):
            results += 1
    
    print(f'Can eventually contain: {results}')

    results = required_to_contain(looking_for, rules, [])

    print(f'Contains total bags: {results}')


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)