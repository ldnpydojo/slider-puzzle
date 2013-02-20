import sys
import math
import pprint
import random
from collections import defaultdict

from board import Board


def a_star_search(b):
    start_score = b.score()
    print 'Scrambled:'
    print 'Score: ', start_score
    print b
    done = defaultdict(lambda: 0)
    done[b.tile_string()] += 1
    fails = 0
    for i in range(1, 5001):
        futures = b.possible_futures()
        unseen_futures = dict((mv, bd) for (mv, bd) in futures.items() if bd.tile_string() not in done)
        move = min(futures.items(),
            key=lambda mv_bd:
                mv_bd[1].score() + \
                # penalise boards we've seen before
                # testing shows 3 to be the most effective multiple here
                3*done[mv_bd[1].tile_string()]
            )[0]
        b.slide(move)
        print '%s Score %s/%s (%s chars of memory): %s/%s/%s' %(
            i, b.score(), start_score, len(str(locals())), len(unseen_futures), len(futures), sum(done.values())
        )
        print 'x'*b.score()
        print b
        if b.check_if_finished():
            break
        done[b.tile_string()] += 1
    print 'Solved!' if b.check_if_finished() else 'Failed'
    print 'From a starting distance of', start_score
    print 'after', i, 'iterations'
    return i

def one_run():
    """
    run python sliding_with_astar.py without args
    then when you get an interesting result, you can read off the
    seed value, and replay that board with
    python sliding_with_astar.py [seed value]
    """
    seed = ''.join(sys.argv[1:]) or str(random.randint(0, 99999))
    random.seed(seed)
    b = get_scrambled_board(4, 99)
    try:
        return a_star_search(b)
    finally:
        print 'seed was', seed

if __name__ == "__main__":
    one_run()
