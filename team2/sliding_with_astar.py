import math
import pprint
import random

class Board:

    @classmethod
    def from_string(cls, picture):
        """
        >>> Board.from_string('12 34') # doctest: +NORMALIZE_WHITESPACE
        1 2
        3
        >>> Board.from_string('12 34').n
        2
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
        1 2 3
        4 5
        7 8 6
        """
        gap = self.find_gap()
        assert tile in self.possible_moves()
        self.board[tile], self.board[gap] = self.board[gap], self.board[tile]
        return self

    def score(self):
        """
        >>> Board.from_string('12 43').score()
        1
        >>> Board.from_string('21 43').score()
        3
        >>> Board.from_string('923 456 781').score()
        8
        """
        score = 0
        correct_board = Board(board=self.correct_board())
        for i in range(self.n):
            for j in range(self.n):
                tile = self.board[(i, j)]
                if tile == self.gap_num:
                    continue
                correct_location = correct_board.find(tile)
                dx = abs(i-correct_location[0])**2
                dy = abs(j-correct_location[1])**2
                score += dx + dy
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
            print '(Score: %s)' % current.score()
            print current
            queue = queue[1:]

            if current.check_if_finished():
                break
            current_hash = hash(current)
            for move in current.possible_moves():
                # print move
                new_board = current.copy().slide(move)
                if current_hash in known or new_board in queue:
                    continue
                queue.append(new_board)
            known[current_hash] = True

        print 'Solved!' if current.check_if_finished() else 'Failed'
        print 'after', iterations, 'iterations\n'


def get_scrambled_board(n, eggs=10):
    b = Board(n)
    b.scramble(eggs)
    return b

def brute_force(b):
    s = Solver()
    s.solve(b)

def a_star_search(b):
    start_score = b.score()
    print 'Scrambled:'
    print 'Score: ', start_score
    print b
    done = set([b.tile_string()])
    fails = 0
    for i in range(362880):
        futures = b.possible_futures()
        unseen_futures = dict((mv, bd) for (mv, bd) in futures.items() if bd.tile_string() not in done)
        if not unseen_futures:
            done = set()
            fails += 1
            print 'no moves left! but keep trying!'
            continue
        move = min(unseen_futures.items(), key=lambda mv_bd:mv_bd[1].score()+random.uniform(0, 0.4))[0]
        b.slide(move)
        print '%s Score %s: %s/%s/%s' %(
            i, b.score(), len(unseen_futures), len(futures), fails
        )
        print 'x'*b.score()
        print b
        if b.check_if_finished():
            break
        done.add(b.tile_string())
    print 'Solved!' if b.check_if_finished() else 'Failed'
    print 'From', start_score
    print 'after', i, 'iterations'


if __name__ == "__main__":
    b = get_scrambled_board(3, 99)
    brute_force(b)
    a_star_search(b)