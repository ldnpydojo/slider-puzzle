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

    def tile_string(self):
        """
        >>> Board(3).tile_string()
        '123456789'
        """
        return ''.join(str(ij_num[1])
            for ij_num in
                sorted(
                    self.board.items(),
                    key=lambda ij_num: list(reversed(ij_num[0]))
                )
            )

    def __repr__(self):
        indent = " "*self.depth
        res = ""
        w = max(map(lambda x:len(str(x)), self.board.values()))+1
        for j in range(self.n):
            res += indent
            for i in range(self.n):
                tile = self.board[(i,j)]
                if tile == self.gap_num:
                    tile = ' '
                res += ("%*s" % (w, tile))

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


    def find(self, num):
        """
        >>> Board(2).find(2)
        (1, 0)
        """
        return [ij for (ij, tile) in self.board.items() if tile==num][0]

    def find_gap(self):
        """
        >>> Board(2).find_gap()
        (1, 1)
        """
        return self.find(self.gap_num)


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

    def possible_futures(self):
        return dict((move, self.copy().slide(move)) for move in self.possible_moves())

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
                if tile != self.correct_tile((i, j)):
                    return False
        return True

    def slide(self, tile):
        """
        >>> Board(3).slide((2, 1)) # doctest: +NORMALIZE_WHITESPACE
        123
        45
        786
        """
        gap = self.find_gap()
        assert tile in self.possible_moves()
        self.board[tile], self.board[gap] = self.board[gap], self.board[tile]
        return self

    def score(self):
        """

        """
        score = 0
        correct_board = Board(board=self.correct_board())
        for i in range(self.n):
            for j in range(self.n):
                tile = self.board[(i, j)]
                if tile == self.gap_num:
                    continue
                correct_location = correct_board.find(tile)
                dx = abs(i-correct_location[0])
                dy = abs(j-correct_location[1])
                score += dx+dy
        return score


    def __eq__(self, other):
        """
        >>> Board(3) == Board(3)
        True
        """
        return self.tile_string() == other.tile_string()

    def __hash__(self):
        """
        >>> b = Board(3)
        >>> b in set([Board(4), Board(5)])
        False
        >>> b in set([Board(3), Board(5)])
        True
        """
        return hash(self.tile_string())

    def scramble(self, n):
        for i in xrange(n):
            move = random.choice(self.possible_moves())
            self.slide(move)

class Solver:

    def __init__(self):
        self.stack = []
        self.known = {}

    def solve(self, board):
        known = {}

        queue = [board]
        current = None
        iterations = 0
        while len(queue):
            iterations += 1
            current = queue[0]
            print len(queue), 'boards to check'
            print 'Score:', current.score()
            print current
            queue = queue[1:]

            if current.check_if_finished():
                print "board is finished"
                break
            current_hash = hash(current)
            for move in current.possible_moves():
                # print move
                new_board = current.copy().slide(move)
                if current_hash in known or new_board in queue:
                    continue
                queue.append(new_board)
            known[current_hash] = True

if __name__ == "__main__":
    b = Board(3)
    for i in range(2):
        moves = b.possible_moves()
        b.slide(random.choice(moves))

    s = Solver()

    s.solve(b)
