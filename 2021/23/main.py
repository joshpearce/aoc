#!/usr/bin/env python3
from copy import deepcopy
from collections import namedtuple
import queue

Move = namedtuple('Move', 'src, dst, steps')

part_2_board = [
    ['.']*11, 
    [c for c in "##C#B#A#D##"],  
    [c for c in "##D#C#B#A##"], 
    [c for c in "##D#B#A#C##"], 
    [c for c in "##B#C#D#A##"]
    ] 

home_rooms = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
home_rooms_lookup = {v:k for k, v in home_rooms.items()}
hallway = list(range(0, 12))
valid_hallway_idxs = [0,1,3,5,7,9,10]
room_idxs = [2,4,6,8]
move_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

hallway_paths_by_room = {
    2: [[1,0], [3,5,7,9,10]], 
    4: [[3,1,0], [5,7,9,10]],
    6: [[5,3,1,0], [7,9,10]],
    8: [[7,5,3,1,0], [9,10]]
}

def settled(board, row, col):
    return home_rooms[board[row][col]] == col and all([board[_row][col] == home_rooms_lookup[col] for _row in range(row+1, 5)])

def room_ready_at(board, col, letter):
    idx = -1
    for row in range(1, 5):
        if board[row][col] == '.':
            idx = row
        elif board[row][col] != letter:
            return -1
    return idx

def all_possible_moves_to_hall(board):
    moves = []
    for room_col in room_idxs:
        for row in [1,2,3,4]:
            if board[row][room_col] != '.':
                if not settled(board, row, room_col):
                    hall_left, hall_right = hallway_paths_by_room[room_col]
                    for hl_col in hall_left:
                        if board[0][hl_col] == '.':
                            move = Move((row, room_col), (0, hl_col), row + room_col - hl_col)
                            moves.append(move)
                        else: break
                    for hr_col in hall_right:
                        if board[0][hr_col] == '.':
                            move = Move((row, room_col), (0, hr_col), row + hr_col - room_col)
                            moves.append(move)
                        else: break
                break
    return moves

def all_possible_moves_to_room(board):
    moves = []
    for hall_col in valid_hallway_idxs:
        if board[0][hall_col] != '.':
            home_room_col = home_rooms[board[0][hall_col]]
            if hall_col < home_room_col:
                hallway_span = hallway[hall_col+1:home_room_col+1]
            else:
                hallway_span = hallway[home_room_col:hall_col]
            if all([board[0][h] == '.' for h in hallway_span]):
                room_row = room_ready_at(board, home_room_col, board[0][hall_col])
                if room_row > 0:
                    move = Move((0, hall_col), (room_row, home_room_col), len(hallway_span) + room_row)
                    moves.append(move)
    return moves

def board_to_tuple(board):
    return tuple(board[0]) + tuple(board[1][2:-2]) + tuple(board[2][2:-2]) + tuple(board[3][2:-2]) + tuple(board[4][2:-2])

def solved(board):
    return (all([board[r][2] == 'A' for r in [1,2,3,4]]) and 
            all([board[r][4] == 'B' for r in [1,2,3,4]]) and
            all([board[r][6] == 'C' for r in [1,2,3,4]]) and
            all([board[r][8] == 'D' for r in [1,2,3,4]]))

if __name__ == "__main__":

    solutions = set()
    seen = set()
    queue = queue.PriorityQueue()
    queue.put((0, part_2_board))

    while not queue.empty():
        energy, board = queue.get()
        energy = -energy
        moves = all_possible_moves_to_hall(board) + all_possible_moves_to_room(board)
        for src, dst, steps in moves:
            new_energy = energy + steps * move_cost[board[src[0]][src[1]]]
            new_board = deepcopy(board)
            new_board[dst[0]][dst[1]] = new_board[src[0]][src[1]]
            new_board[src[0]][src[1]] = '.'
            if solved(new_board):
                solutions.add(new_energy)
                print(min(solutions))
                print(f"queue size {queue.qsize()}")
            else:
                board_tuple = board_to_tuple(new_board)
                if (board_tuple, new_energy) not in seen:
                    queue.put((-new_energy, new_board))
                    seen.add((board_tuple, new_energy))

    print()
    print(min(solutions))
    print(len(seen))
        
