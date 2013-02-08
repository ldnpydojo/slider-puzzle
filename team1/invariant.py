#!/usr/bin/env python

from itertools import combinations, permutations
from collections import defaultdict

SAMPLE_BOARD = {
    0: {0: 1, 1: 2, 2: 3},
    1: {0: 4, 1: 5, 2: 6},
    2: {0: 7, 1: 8, 2: None}
}

BAD_BOARD = {
    0: {0: 1, 1: 2, 2: 3},
    1: {0: 4, 1: 5, 2: 6},
    2: {0: 8, 1: 7, 2: None}
}


def generate_trivial_boards():
    tiles = [1, 2, 3, None]
    tile_combos = permutations(tiles, 4)
    for c in tile_combos:
        tiles = list(c)
        board = defaultdict(dict)
        for i in range(2):
            for j in range(2):
                board[i][j] = tiles[2 * i + j]
        yield board

def main():
    print "good board", check_invariant(SAMPLE_BOARD)
    print "bad board", check_invariant(BAD_BOARD)
    for b in generate_trivial_boards():
        print b, "=>", check_invariant(b)


def check_invariant(board):
    parity = determine_parity_permutation(board)
    #print "parity: %s" % parity
    taxicab = determine_taxi_cab(board)
    #print "taxicab: %s" % taxicab
    return parity == taxicab


def determine_parity_permutation(board):
    """Board parity is the evenness of the number of instances
    where one tile is greater than a later tile in the sequence
    reading from top-left to bottom-right.
    """
    tiles_sequence = []
    n = len(board)
    for i in range(n):
        for j in range(n):
            tiles_sequence.append(board[i][j])

    #print tiles_sequence
    combos = combinations(tiles_sequence, 2)

    inversions = [(i, j) for (i, j) in combos if (j > i) and (i is not None) and (j is not None)]
    #print "inversions: ", inversions
    return not bool(len(inversions) % 2)


def determine_taxi_cab(board):
    """Taxicab distance is the sum of horizontal and
    vertical moves between the blank square and the
    bottom-right corner of the grid. We return its
    parity (whether it's even).
    """
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] is None:
                break

    dx = (n - 1) - i
    dy = (n - 1) - j
    return not bool((dx + dy) % 2)

if __name__ == '__main__':
    main()
