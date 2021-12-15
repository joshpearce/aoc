#!/usr/bin/env python3
from itertools import product
import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_neighbors(x, y, mx, my, forward_only=True, diagonal=False):
    back = 0 if forward_only else -1
    if diagonal:
        return { *list(product(
            range(max(x + back, 0), min(x + 1, mx) + 1), 
            range(max(y + back, 0), min(y + 1, my) + 1))) } - {(x, y)}
    else:
        return set(
            [(i, y) for i in range(max(x + back, 0), min(x + 2, mx))] + 
            [(x, j) for j in range(max(y + back, 0), min(y + 2, my))]
        ) - {(x, y)}

def print_grid(grid, highlights=[], code=bcolors.FAIL):
    print()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) in highlights:
                print(f"{code}{grid[i][j]}{bcolors.ENDC}", end="")
            else:
                print(f"{grid[i][j]}", end="")
        print()
    print()


def part_one(grid):
    from dijkstar import Graph, find_path
    mx, my = len(grid), len(grid[0])
    graph = Graph()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ns = get_neighbors(i, j, mx, my, forward_only=False)
            for n in ns:
                graph.add_edge((i, j), n, grid[n[0]][n[1]])
    
    def cost_func(u, v, edge, prev_edge):
        return edge

    path = find_path(graph, (0, 0), (mx-1, my-1), cost_func=cost_func)

    print_grid(grid, highlights=path.nodes)

    return path.total_cost
    
def part_one_a(grid):
    from queue import PriorityQueue

    class Graph:
        def __init__(self, num_of_vertices):
            self.v = num_of_vertices
            self.edges = {}
            self.visited = []
        
        def add_edge(self, u, v, weight):

            if u in self.edges:
                self.edges[u][v] = weight
            else:
                self.edges[u] = {v: weight}

    def dijkstra(graph, start_vertex, end_vertex):
        D = {v:float("inf") for v in graph.edges.keys()}
        D[start_vertex] = 0

        pq = PriorityQueue()
        pq.put((0, start_vertex))

        while not pq.empty():
            (dist, current_vertex) = pq.get()
            graph.visited.append(current_vertex)

            for neighbor, distance in graph.edges[current_vertex].items():
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
        return D    

    mx, my = len(grid), len(grid[0])
    graph = Graph(mx * my) 
    for i in range(len(grid)):
        for j in range(len(grid)):
            ns = get_neighbors(i, j, mx, my, forward_only=False)
            for n in ns:
                graph.add_edge((i, j), n, grid[n[0]][n[1]])
    
    result = dijkstra(graph, (0, 0), (mx-1, my-1))
    return result[(mx-1, my-1)]
        
def part_two(grid):

    gl = len(grid)
    big_grid = np.zeros((gl*5, gl*5), dtype=np.int)
    big_grid[0:gl, 0:gl] = grid
    for i in range(1,5):
        s = big_grid[(i-1)*gl:i*gl, 0:gl]
        big_grid[i*gl:(i+1)*gl, 0:gl] = np.array([[max(1, (x+1)%10) for x in r] for r in s])
    for i in range(1,5):
        s = big_grid[0:5*gl, (i-1)*gl:i*gl]
        big_grid[0:5*gl, i*gl:(i+1)*gl] = np.array([[max(1, (x+1)%10) for x in r] for r in s])
    
    return part_one(big_grid)

if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    f = "input.txt"
    lines = (Path(__file__).parent / f).open().read().split("\n")
    g = [list(map(int,l)) for l in lines]
    

    
    #print("\nPart one:")
    #print(f"{part_one_a(g)}")

    print("Part two:")
    print(f"{part_two(g)}")
    