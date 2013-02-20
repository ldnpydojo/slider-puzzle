import os
import sys
import random
from collections import defaultdict

from board import Board


def a_star_search(b):
    start_score = b.score()
    print 'Scrambled:'
    print 'Score: ', start_score
    print b
    done = set([b.tile_string()])
    horizon = defaultdict(list)
    best_board = b
    best_score = b.score()
    worst_score = b.score()
    for loop_num in range(1, 50001):
        futures = b.possible_futures()
        unseen_futures = dict((mv, bd) for (mv, bd) in futures.items() if bd.tile_string() not in done)
        [horizon[bd.score()].append(bd) for (mv, bd) in unseen_futures.items()]

        if not horizon:
            print 'no moves on the horizon'
            return
        lowest_score, possible_tries = min((scr, bds) for (scr, bds) in horizon.items() if bds)

        num_best = len(possible_tries)
        b = possible_tries.pop(0)
        score = b.score()
        if score <= best_score:
            best_score = score
            best_board = b
        worst_score = max(worst_score, score)
        done.add(b.tile_string())
        msg = '%3s Depth: %3s\nMoves:\n\tBest unseen %3s @ %3s\n\tHere %3s/%3s (best/new/seen)\n\tEverywhere %3s/%3s (horizon/done)\n\t(%s chars of memory)\nScore:\n\t%3s/%3s/%3s/%3s (score/best/start/worst)\n' %(
            loop_num, b.depth, num_best, lowest_score, len(unseen_futures), len(futures), len(horizon), len(done),len(str(locals())), score, best_score, start_score, worst_score
        )
        os.system('clear')
        print msg
        char_dict = {best_score:'<', score:'X', start_score:'^', worst_score:'>'}
        print 'score:', ''.join(char_dict.get(i, '-') for i in range(worst_score+1))
        print 'Current:\n', b
        print
        print 'Best yet:\nScore: ', best_score, '\n', best_board,
        if b.check_if_finished():
            break

    print '\n'.join(b.history)
    print msg
    print 'Solved!' if b.check_if_finished() else 'Failed'
    print 'From a starting distance of', start_score
    print 'after', b.depth+1, 'moves and', loop_num, 'iterations'
    return loop_num

def one_run():
    """
    run python sliding_with_astar.py without args
    then when you get an interesting result, you can read off the
    seed value, and replay that board with
    python sliding_with_astar.py [seed value]
    """
    seed = ''.join(sys.argv[1:]) or str(random.randint(0, 99999))
    random.seed(seed)
    b = Board.get_scrambled(4, 99)
    try:
        return a_star_search(b)
    finally:
        print 'seed was', seed

if __name__ == "__main__":
    one_run()
