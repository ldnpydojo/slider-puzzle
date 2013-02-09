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
        self.board = board or self.correct_board()
        self.depth = depth
        self.gap_num = max(self.board.values())

    def copy(self):
        """
        >>> b = Board(3)
        >>> id(b) != id(b.copy())
        True
        """
        return Board(self.n, self.board.copy(), self.depth+1)

    def __repr__(self):
        indent = " "*self.depth
        res = ""
        for j in range(self.n):
            res += indent
            for i in range(self.n):
                tile = self.board[(i,j)]
                if tile != self.gap_num:
                    res += "%s" % tile
                else:
                    res += ' '
            res += "\n"
        return res

    def correct_tile(self, ij):
        """
        >>> Board(2).correct_tile((1, 0))
        2
        """
        i, j = ij
        return j*self.n + i + 1

    def correct_board(self):
        return dict(((i,j), self.correct_tile((i,j))) for i in range(self.n) for j in range(self.n))


    def find_gap(self):
        """
        >>> Board(2).find_gap()
        (1, 1)
        """
        return [ij for (ij, tile) in self.board.items() if tile==self.gap_num][0]


    def possible_moves(self):
        """
        >>> Board(2).possible_moves()
        [(0, 1), (1, 0)]
        """
        res = []
        gap = self.find_gap()

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
        """
        >>> Board.from_string('12 34').check_if_finished()
        True
        >>> Board.from_string('21 34').check_if_finished()
        False
        """
        tile_list = []
        for j in range(self.n):
            for i in range(self.n):
                tile = self.board[(i, j)]
                if tile != self.correct_answer((i, j)):
                    return False
        return True

    def slide(self, tile):
        """
        >>> Board(3).slide((2, 1))
        123
        45
        786
        """
        gap = b.find_gap()
        assert tile in self.possible_moves()
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
