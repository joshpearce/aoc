#!/usr/bin/env python3
from aocd.models import Puzzle
from collections import Counter

card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}

def card_value(c):
    if c.isdigit():
        return int(c)
    else:
        return card_values[c]

def tiebreaker_val(hand):
    val = 0
    m = 14**5
    for c in hand:
        val += m * card_value(c)
        m = m / 14
    return val

def hand_key(hand, orig_hand=None):
    tie_hand = hand
    if orig_hand:
        tie_hand = orig_hand
    freq = Counter(hand)
    freq_vals = sorted(freq.values(), reverse=True)
    most_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[0][0]

    if not orig_hand and freq_vals[0] != 5:
        if 'J' in freq:
            if most_freq == 'J':
                second_most_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[1][0]
                return hand_key(hand.replace('J', second_most_freq), orig_hand=hand)
            else:
                return hand_key(hand.replace('J', most_freq), orig_hand=hand)

    val = 0
    if freq_vals[0] == 5:
        val = 1000000000000 + tiebreaker_val(tie_hand)
    elif freq_vals[0] == 4:
        val = 100000000000 + tiebreaker_val(tie_hand)
    elif freq_vals[0] == 3:
        if freq_vals[1] == 2:
            val = 10000000000 + tiebreaker_val(tie_hand)
        else:
            val = 1000000000 + tiebreaker_val(tie_hand)
    elif freq_vals[0] == 2:
        if freq_vals[1] == 2:
            val = 100000000 + tiebreaker_val(tie_hand)
        else:
            val = 10000000 + tiebreaker_val(tie_hand)
    else:
        val = tiebreaker_val(tie_hand)


    return val
    

def part_a(lines):

    s1 = hand_key('59234')
    s2 = hand_key('58AKQ')

    hand_bids = sorted([tuple(l.split()) for l in lines], key=lambda h: hand_key(h[0]))
    total_winnings = sum((x[0]+1) * int(x[1][1]) for x in enumerate(hand_bids))

    return total_winnings

def part_b(lines):
    return None


puzzle = Puzzle(year=2023, day=7)
UseExampleData = False
data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data
lines = data.split('\n')

ans_a = part_a(lines)
if not puzzle.answered_a:
    puzzle.answer_a = ans_a


card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10}

ans_b = part_a(lines)
if not puzzle.answered_b:
    puzzle.answer_b = ans_b
