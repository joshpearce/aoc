from collections import Counter
from itertools import chain
from aocd.models import Puzzle


VALUE_MAP = {
	str(c): i
	for i, c in enumerate(
		chain(range(2, 10), 'TJQKA'),
		start=2,
	)
}
JOKER_VALUE_MAP = VALUE_MAP | {'J': 0}

def score_hand(hand, jokers=False):
	counts = Counter(hand)
	
	if jokers: j_count, value_map = counts.pop('J', 0), JOKER_VALUE_MAP
	else: j_count, value_map = 0, VALUE_MAP
	
	rank = tuple(sorted(counts.values(), reverse=True))
	if j_count: rank = ((rank[0] + j_count,) + rank[1:]) if rank else (j_count,)
	
	return rank + tuple(value_map[c] for c in hand)

def calculate_winnings(lines, jokers=False):
	return sum(
		rank * bid
		for rank, bid in enumerate(
			(
				bid for score, bid in sorted(
					(score_hand(hand, jokers), int(bid))
					for hand, bid in (line.split(' ') for line in lines)
				)
			),
			start=1,
		)
	)

def solve_one(lines): return calculate_winnings(lines)
def solve_two(lines): return calculate_winnings(lines, jokers=True)


puzzle = Puzzle(year=2023, day=7)
UseExampleData = False
data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data
lines = data.split('\n')
solve_one(lines)
