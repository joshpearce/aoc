#!/usr/bin/env python3

from functools import reduce
from itertools import product
from operator import mul


def adjacent_points(grid, x, y):
	return {
		(min(len(grid[y]) - 1, x + 1), y),
		(max(0, x - 1), y),
		(x, min(len(grid) - 1, y + 1)),
		(x, max(0, y - 1)),
	} - {(x, y)}


def find_low_points(grid):
	return (
		(x, y)
		for x, y in product(range(len(grid[0])), range(len(grid)))
		if all(
			grid[adj_y][adj_x] > grid[y][x]
			for adj_x, adj_y in adjacent_points(grid, x, y)
		)
	)


def solve_one(lines):
	grid = [[int(c) for c in row] for row in lines]
	
	return sum(grid[y][x] + 1 for x, y in find_low_points(grid))


def flood_fill(grid, x, y):
	visited, new = set(), {(x, y)}
	
	while new:
		x, y = new.pop()
		visited.add((x, y))
		
		new |= {
			(adj_x, adj_y)
			for adj_x, adj_y in adjacent_points(grid, x, y) - visited
			if grid[adj_y][adj_x] != 9
		}
	
	return visited


def solve_two(lines):
	grid = [[int(c) for c in row] for row in lines]
	
	return reduce(
		mul,
		sorted(len(flood_fill(grid, x, y)) for x, y in find_low_points(grid))[-3:]
	)


if __name__ == '__main__':
	import os
	
	cwd = os.path.dirname(os.path.realpath(__file__))
	
	inputs = [
		[l[:-1] for l in open(os.path.join(cwd, f)).readlines()]
		for f in ('test.txt', 'input.txt')
	]
	
	print('One:\n\t' + '\n\t'.join(str(solve_one(i)) for i in inputs))
	print('Two:\n\t' + '\n\t'.join(str(solve_two(i)) for i in inputs))