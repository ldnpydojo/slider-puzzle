import math
import pprint
import random

class Board:

    @classmethod
    def from_string(cls, picture):
        """
        >>> Board.from_string('12 34') # doctest: +NORMALIZE_WHITESPACE
        12
        3
        """
        b = {}
        i, j = 0, 0
        for ch in picture:
            if not ch.strip():
                # new row
                i = 0
                j += 1
            else:
                # new tile
                b[(i, j)] = int(ch)
                i += 1
        return cls(board=b)

    def __init__(self, n=None, board=None, depth=0):
        self.n = n or int(math.sqrt(len(board)))
        self.depth = depth
        self.board = dict(((i,j),j*n+i) for i in range(n) for j in range(n))
        self.gap_num = self.n**2 - 1

    def copy(self):
        b = Board(self.n, self.depth+1)
        b.board = self.board.copy()
        return b

    def __repr__(self):
        indent = " "*self.depth
        res = ""
        for j in range(self.n):
            res += indent
            for i in range(self.n):
                number = self.board[(i,j)]
                if number != self.gap_num:
                    res += "%s" % (number + 1)
                else:
                    res += ' '
            res += "\n"
        return res

    def find_gap(self):
        gap = None
        for j in  range(self.n):
            for i in range(self.n):
                    pos = (i,j)
                    if self.board[pos] == self.gap_num:
                        gap = pos
                        break
            if gap is not None:
                break
        assert gap != None
        return gap


    def possible_moves(self):
        res = []
        gap = self.find_gap()
        print "gap:",gap

        (i,j) = gap
        if i >= 1:
            res.append((i-1, j))
        if i < self.n-1:
            res.append((i+1, j))
        if j >= 1:
            res.append((i, j-1))
        if j < self.n-1:
            res.append((i, j+1))
        assert len(res) > 0

        return res

    def check_if_finished(self):
        number_list = []
        for j in range(self.n):
            for i in range(self.n):
                number = self.board[(i, j)]
                if number != j*self.n + i:
                    return False
        return True

    def slide(self, tile):
        gap = b.find_gap()
        self.board[tile], self.board[gap] = self.board[gap], self.board[tile]
        return self

    def hash(self):
        return str(sorted(self.board.items()))

class Solver:

    def __init__(self):
        self.stack = []
        self.known = {}

    def solve(self, board):
        known = {}

        queue = [board]
        current = None
        while len(queue):
            current = queue[0]
            print current
            print len(queue)
            queue = queue[1:]

            if current.check_if_finished():
                print "board is finished"
                break
            current_hash = current.hash()
            for move in current.possible_moves():
                print move
                new_board = current.copy().slide(move)
                if current_hash in known or new_board in queue:
                    continue
                queue.append(new_board)
            known[current_hash] = True
        print current
        print current.check_if_finished()



if __name__ == "__main__":
    b = Board(3)
    for i in range(2):
        moves = b.possible_moves()
        b.slide(random.choice(moves))

    s = Solver()

    s.solve(b)
