from collections import defaultdict
from copy import deepcopy
from random import choice
import sys

__author__ = 'drake'

width = int(sys.argv[1])
UP, DOWN, LEFT, RIGHT = xrange(4)

def makeSlider(width):
    slider = defaultdict(dict)
    for n in range(width ** 2):
        slider[n % width][int(n / width)] = n
    slider[width-1][width-1] = None
    return slider

def findNone(slider):
    for x in range(len(slider)):
        for y in range(len(slider)):
            if slider[x][y] is None:
                return x, y

def moveTile(slider, direction):
    slider = deepcopy(slider)
    x, y = findNone(slider)

    try:
        if direction is DOWN:
            slider[x][y] = slider[x][y-1]
            slider[x][y-1] = None
        if direction is UP:
            slider[x][y] = slider[x][y+1]
            slider[x][y+1] = None
        if direction is LEFT:
            slider[x][y] = slider[x+1][y]
            slider[x+1][y] = None
        if direction is RIGHT:
            slider[x][y] = slider[x-1][y]
            slider[x-1][y] = None
    except KeyError:
        return None


    return slider

def enumerateSuccessors(slider):
    out = []
    for n in range(4):
        if moveTile(slider, n) is not None:
            out.append(moveTile(slider, n))
    return out

def shuffle(slider, n=50):
    slider = deepcopy(slider)
    for i in xrange(n):
        slider = choice(enumerateSuccessors(slider))
    return slider

def solved(slider):
    return slider == makeSlider(len(slider))

def makePath(history, successor):
    out = [successor]
    while str(successor) in history.keys():
        out = [history[str(successor)]] + out
        successor = history[str(successor)]
    return out

def solve(slider):
    history = {}
    todo = [slider]
    while True:
        sliders = list(todo)
        todo = []
        print len(sliders)
        for slider in sliders:
            successors = enumerateSuccessors(slider)
            for successor in successors:
                if successor in history.keys():
                    continue
                history[str(successor)] = slider
                if solved(successor):
                    return makePath(history, successor)
                todo.append(successor)



s = makeSlider(width)
s = shuffle(s)
#print s
#print findNone(s)
#print moveTile(s, DOWN)
#print s
#print moveTile(s, RIGHT)
#print s
#print moveTile(moveTile(s, DOWN), DOWN)
#print enumerateSuccessors(moveTile(moveTile(s, RIGHT), DOWN))
#print solve(shuffle(s))
print solve(s)