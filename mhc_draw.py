# Draw algorithm for My Horse Connect
#
# Input:
# [list of events, each with a horse and rider]
# [interval indicating minimum space between 2 events with the same horse or rider]
#
# Output:
# [ordered list of events]
# [events that could not be scheduled]
#
# greedy algorithm spacing events
# greedy choice = 
#
#
# example set:
# {Event(1, 1), Event(2, 2), Event(3, 3), Event(2, 4), Event(1, 3), Event(4, 2)}, interval = 3
# Event(1, 1), Event(3, 3), Event(2, 2), Event()
#

from copy import deepcopy
from operator import is_
import random
from dataclasses import dataclass

@dataclass 
class Draw:
    rider: int # stored as int IDs
    horse: int # stored as int IDs

# checks list of draws, returns None if legal, first illegal event if is illegal list
def is_legal(draws: list, interval: int) -> Draw:
    if interval == 0:
        return None
    i = 0
    j = 1
    while j<len(draws) :
        #print(f'i, j : {i, j}')
        for k in range(i, j):
            if draws[k].rider == draws[j].rider or draws[k].horse == draws[j].horse:
                # same rider or horse too close together
                return draws[j]
        if j-i > interval-1:
            i += 1
            j += 1
        else:
            j += 1
    return None

# generates draw order by assigning draw numbers to riders, and doing swaps with rider draw numbers closer than interval spaced apart
def swap_draw(draws: list, interval: int) -> list:
    draw_order = deepcopy(draws)
    random.shuffle(draw_order) # randomize draw order
    iterations = 0
    while(is_legal(draw_order, interval) != None and iterations<100000):
        for i in range(len(draw_order)):
            r, h = draw_order[i].rider, draw_order[i].horse
            for j in range(i+1, len(draw_order)):
                if (draw_order[j].rider == r or draw_order[j].horse == h) and j-i < interval+1:
                    # swap item at j with item min legal distance away from j
                    swap_index = (i+interval+1) if (i+interval+1) < len(draw_order) else (i+interval+1) - len(draw_order)
                    tmp = draw_order[swap_index] 
                    draw_order[swap_index] = draw_order[j]
                    draw_order[j] = tmp
        iterations += 1
    if(is_legal(draw_order, interval) == None):
        return draw_order
    else:
         return None       

# swap draw with decrementing interval each time, returns draw order
def decrementing_swap_draw(draws: list) -> list:
    interval = len(draws) // 5
    draw_order = deepcopy(draws)
    random.shuffle(draw_order) # randomize draw order
    while(interval > 0):
        for i in range(len(draw_order)):
            r, h = draw_order[i].rider, draw_order[i].horse
            for j in range(i+1, len(draw_order)):
                if (draw_order[j].rider == r or draw_order[j].horse == h) and j-i < interval+1:
                    # swap item at j with item min legal distance away from j
                    swap_index = (i+interval+1) if (i+interval+1) < len(draw_order) else (i+interval+1) - len(draw_order)
                    tmp = draw_order[swap_index] 
                    draw_order[swap_index] = draw_order[j]
                    draw_order[j] = tmp
        interval -= 1
    return draw_order

# generates random draw orders until a legal one is found or it gives up
def random_draw(draws: list, interval: int) -> list:
    draw_order = deepcopy(draws)
    for i in range(1000000):
        random.shuffle(draw_order)
        if is_legal(draw_order, interval) == None:
            print(f'interval: {interval}, iteration: {i}')
            return draw_order
    return None

test_events = []
for i in range(100):
    r = random.randint(1, 50)
    test_events.append(Draw(r, r))

#test_events = [Draw(13, 13), Draw(1, 1), Draw(15, 15), Draw(13, 13), Draw(3, 3), Draw(10, 10), Draw(13, 13), Draw(4, 4), Draw(10, 10), Draw(12, 12), Draw(4, 4), Draw(14, 14), Draw(12, 12), Draw(6, 6), Draw(13, 13)]

# print events
for e in test_events:
    print(e.horse, e.rider, end=' | ')
print()
print(f'is legal with interval=0? {is_legal(test_events, 0)}')
print()

# for i in range(1,8):
#     print(f'find random draw with interval={i}: ')
#     test_events_i = random_draw(test_events, i)
#     if test_events_i != None:
#         for e in test_events_i:
#             print(e.horse, e.rider, end=' | ')
#         print()
#     else:
#         print('no draw found')
#     print(f'find swap draw with interval={i}: ')
#     test_events_i = swap_draw(test_events, i)
#     if test_events_i != None:
#         for e in test_events_i:
#             print(e.horse, e.rider, end=' | ')
#         print()
#     else:
#         print('no draw found')
#     print()

print()
print(f'decrementing swap draw:')
test_events_i = decrementing_swap_draw(test_events)
for e in test_events_i:
    print(e.horse, e.rider, end=' | ')
print()
for i in range(0, len(test_events) // 5):
    if is_legal(test_events_i, i) != None:
        print(f'interval: {i}')
        break