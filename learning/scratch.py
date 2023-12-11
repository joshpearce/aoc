#!/usr/bin/env python

import itertools as it

bets = (
'w_a',
'w_b',
'w_c',
'w_d',
'd_a',
'd_b',
'd_c',
'd_d')

comb_2 = list(it.combinations(bets, 2))
comb_3 = list(it.combinations(bets, 3))
comb_4 = list(it.combinations(bets, 4))

comb_4_filtered = []
for c in comb_4:
        if len(set([p[1:] for p in c])) == 4:
            comb_4_filtered.append(c)

pass