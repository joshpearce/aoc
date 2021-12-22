#!/usr/bin/env python3

# Better code here: https://topaz.github.io/paste/#XQAAAQDJBwAAAAAAAAAzHIoib6p4r/McpYgEEgWhHoa5LSRMkUrBIsXZrdB/Mf/iNcpW7Crh0Hab6aE4/2sYY7m2WQRa4zRwNeMv1i9zovm5Z7/CuzwHvnFrAJ6EAD9OMHKJo72Mq2fsXDIXaq/ygcQlT4Sy5DU7gMfDseOrS8JC+Cu87/h/54/vqWVsCo9+47wzpmJa1BlHOySFH00jevhknzVaQEEgDI6GPgq1Jt5BpB2uK2fv6x7iYLvnrl1eR1wuqE2AvDlb5O0OMv4I44CReMRcan3riF2Z0xNqE2MiWDHCa2a2tvPQ34uSTdJUdCoIr+gxDg1QC3bid2tBAv2P0QWDEBs+zoU/HdtHMzsLVkaRk9nhnOJ31yJRqmwxkC1Z6roojGMgpv7xPev/c+QPd1mC4hPeSswLlvl+yPXLboDcoRBHtsSWiK4mFw4VatIq1U/QDyAZe/kMe6TTbWVjhEUQANEj6e8LS9gfrxYmWEkgtvvfE5x7vJPiDAOkqjgxkq1arHSMGFHw0cH8LSUCPMv5CGRaRoL/tE7LzaSJSoUsPLo9Wn3YhaN0JUfr2hipD6Y4zl6Ncs4QYCz2/kye307QC+Fp1nxD30gWDHkYYVeoHST1Bl5XuUvXpF0i4Y8welumgC1FMzjVfnqH4Kh+4r/QBfyvVxu5QoV5Fvg5prB3wLv4ORC9x1/Oz+4dE6N0f0sN6PpDyvgkqAOOe/Her3tCcTwCBlw9hcCMlfM2M3z7nm6ym3y+anm0Qblkxc3uuCllFoKxwiKSstkMZEVPe5KvTM+I3AQk2BpkgzvMn4wmuxugYRXOiD/n4Q3EWq+F5Z0WmhVdCAZ8KYD99zfeFsAj+f9ZCVGPkGUiyq2ien9VzpqtWWqGrSCMI2hfzSSNlQSBjondlHYOztARWjR/obcdFQjfU/tjbYU1dW/FAA+jJUBxzCvHkEXCiQYSdAf5RP/3aMiU

from collections import defaultdict, namedtuple
import re
from functools import lru_cache
import copy

Player = namedtuple('Player', 'name, pos, score')

def move(cur, inc, mod=10):
    return (cur + inc -1) % mod +1

class DeterministicDie:
    def __init__(self, max=100):
        self.max = max
        self.cur = 0
        self.count = 0
    
    def roll(self):
        self.count += 1
        self.cur = self.cur % self.max + 1
        return self.cur
    
    def rolln(self, n):
        for _ in range(n):
            yield self.roll()

def part_one(players):
    die = DeterministicDie()
    done = False
    while not done:
        for i, p in enumerate(players):
            rolls = list(die.rolln(3))
            sumrolls = sum(rolls)
            pos = move(p.pos, sumrolls)
            score = p.score + pos
            players[i] = Player(p.name, pos, score)
            #print(f"Player {p.name} rolls {'+'.join(map(str, rolls))} and moves to space {pos} for a total score of {score}.")
            if score >= 1000:
                done = True
                break
    return die.count * min(p.score for p in players)



#         1                    2                    3
#  1      2      3      1      2      3      1      2      3
#1 2 3  1 2 3  1 2 3  1 2 3  1 2 3  1 2 3  1 2 3  1 2 3  1 2 3 
@lru_cache(maxsize=None)
def gen3rolluniverses(depth=2):
    l = [[1], [2], [3]]
    for _ in range(depth):
        nl = []
        for r in l:
            for i in [[1], [2], [3]]:
                nl.append(r+i)
                l = nl
    return l
            

def part_two(players):
    Unistate = namedtuple('Unistate', 'p1_pos, p2_pos, p1_score, p2_score, p1_next')
    top_state = defaultdict(int)
    top_state[Unistate(players[0].pos, players[1].pos, players[0].score, players[1].score, True)] = 1
    player1_wins, player2_wins = 0, 0
    while True:
        for p1_turn in [True, False]:
            new_universes = [copy.deepcopy(top_state) for _ in range(27)]
            all_uni_rolls = gen3rolluniverses()
            for i, rolls in enumerate(all_uni_rolls):
                temp_state = defaultdict(int)
                for state, count in new_universes[i].items():
                    if p1_turn:
                        if state.p1_next == p1_turn:
                            sumrolls = sum(rolls)
                            p1_pos = move(state.p1_pos, sumrolls)
                            p1_score = state.p1_score + p1_pos
                            if p1_score >= 21:
                                player1_wins += count
                            else:
                                new_state = Unistate(p1_pos, state.p2_pos, p1_score, state.p2_score, False)
                                temp_state[new_state] = count
                        else:
                            temp_state[state] = count
                    else:
                        if state.p1_next == p1_turn:
                            sumrolls = sum(rolls)
                            p2_pos = move(state.p2_pos, sumrolls)
                            p2_score = state.p2_score + p2_pos
                            if p2_score >= 21:
                                player2_wins += count
                            else:
                                new_state = Unistate(state.p1_pos, p2_pos, state.p1_score, p2_score, True)
                                temp_state[new_state] = count
                        else:
                            temp_state[state] = count
                new_universes[i] = temp_state
            top_state = defaultdict(int)
            for uni in new_universes:
                for k, v in uni.items():
                    top_state[k] += v
            if len(top_state) == 0:
                return max(player1_wins, player2_wins)
            pass
        

    

if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    f = "input.txt"

    lines = (Path(__file__).parent / f).open().read().split("\n")
    
    players = [Player(f"player{i}", int(re.findall('[0-9]+', l)[1]), 0) for i, l in enumerate(lines)]
    print("\nPart one:")
    print(f"{part_one(players)}")

    players = [Player(f"player{i}", int(re.findall('[0-9]+', l)[1]), 0) for i, l in enumerate(lines)]
    print("Part two:")
    print(f"{part_two(players)}")
    
