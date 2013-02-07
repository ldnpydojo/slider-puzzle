from collections import defaultdict
import random

EMPTY = ' '


def random_slider(n, randomize=random.shuffle):
    l = range(n ** 2 - 1)
    randomize(l)
    l.append(EMPTY)
    slider = defaultdict(dict)
    for i in range(n):
        for j in range(n):
            slider[i][j] = l[i * n + j]
    return slider


def ordered_slider(n):
    return random_slider(n, randomize=lambda x: x)


def print_slider(slider):
    for i in range(len(slider)):
        print ' '.join(str(c) for c in slider[i].values())


def check_slider(slider):
    n = len(slider)
    for i in range(n):
        for j in range(n):
            assert slider[i][j] == (EMPTY if i == n - 1 and j == n - 1 else i * n + j)
