from collections import defaultdict
import random


def random_board(n, randomize=random.shuffle):
    l = range(n**2 - 1)
    randomize(l)
    l.append(-1)
    b = defaultdict(dict)
    for i in range(n):
        for j in range(n):
            b[i][j] = l[i*n+j]
    return b


def ordered_board(n):
    return random_board(n, randomize=lambda x: x)


def print_board(b):
    for i in range(len(b)):
        print ' '.join(str(c) for c in b[i].values())


def check_board(b):
    n = len(b)
    for i in range(n):
        for j in range(n):
            assert b[i][j] == (-1 if i == n-1 and j == n-1 else i*n+j)


def test_check_ordered_board():
    check_board(ordered_board(3))

if __name__ == '__main__':
    print_board(ordered_board(3))
    print_board(random_board(3))
