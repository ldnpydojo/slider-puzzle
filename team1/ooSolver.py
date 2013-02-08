from collections import defaultdict
from copy import deepcopy
from random import choice
import sys

UP, DOWN, LEFT, RIGHT = xrange(4)

class Board(object):
    def __init__(self, width):
        self.width = width
        self.board = defaultdict(dict)
        for n in range(self.width ** 2):
            self.board[n % width][int(n / width)] = n
        self.board[width-1][width-1] = None

    def copy(self):
        out = Board(self.width)
        out.board = deepcopy(self.board)
        return out

    def get(self, x, y):
        return self.board[x][y]
    
    def __str__(self):
        s = []
        for y in range(self.width):
            out = []
            for x in range(self.width):
                out.append(str(self.board[x][y]) if self.board[x][y] is not None else " ")
            s.append(" ".join(out))
        return "\n".join(s)

    def findNone(self):
        for x in range(self.width):
            for y in range(self.width):
                if self.board[x][y] is None:
                    return x, y

    def moveTile(self, direction):
        board = self.copy()
        x, y = self.findNone()
    
        try:
            if direction is DOWN:
                board.board[x][y] = board.board[x][y-1]
                board.board[x][y-1] = None
            if direction is UP:
                board.board[x][y] = board.board[x][y+1]
                board.board[x][y+1] = None
            if direction is LEFT:
                board.board[x][y] = board.board[x+1][y]
                board.board[x+1][y] = None
            if direction is RIGHT:
                board.board[x][y] = board.board[x-1][y]
                board.board[x-1][y] = None
        except KeyError:
            return None
    
        return board

    def up(self):
        return self.moveTile(UP)

    def down(self):
        return self.moveTile(DOWN)

    def left(self):
        return self.moveTile(LEFT)

    def right(self):
        return self.moveTile(RIGHT)

    def possibleMoves(self):
        out = []
        for n in range(4):
            if self.moveTile(n) is not None:
                out.append(self.moveTile(n))
        return out

    def shuffle(self, n=100):
        out = self
        for i in xrange(n):
            out = choice(out.possibleMoves())
        return out

    def score(self):
        s = 0
        for n in range(self.width ** 2):
            if self.board[n % self.width][int(n / self.width)] == n:
                s += 1
        return self.width ** 2 - 1 - s

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

def makePath(history, current):
    if current in history.keys():
        return makePath(history, history[current]) + [current]
    return [current]

def solve(start):
    closed = set()
    open = set()
    open.add(start)
    cameFrom = {}

    n=0
    while len(open) > 0:
        sys.stdout.write(spin(int(n/10)))
        sys.stdout.flush()
        n += 1

        current = min(open, key=lambda x: x.score())
        if current == Board(current.width):
            return makePath(cameFrom, current)

        open.discard(current)
        closed.add(current)

        for neighbour in current.possibleMoves():
            if neighbour in closed:
                continue
            if not neighbour in open:
                cameFrom[neighbour] = current
                open.add(neighbour)

    return []

def spin(n):
    return '\b' + "\\-/|"[n % 4]

def main(n):
    b = Board(n).shuffle()
    print "Start:"
    print b
    print
    s = solve(b)
    print "SOLVED"
    n = 0
    for step in s:
        print "Step", n
        print step
        print
        n += 1

def test():
    print Board(2)
    print Board(2) == Board(2)
    print Board(2).__hash__()
    print Board(2).__hash__()

if __name__=="__main__":
    while True: main(int(raw_input("Width:")))
    #test()