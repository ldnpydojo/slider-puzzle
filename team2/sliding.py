import pprint

class Board:

    def __init__(self, n):
        self.n = n
        self.board = dict(((i,j),j*n+i) for i in range(n) for j in range(n))
        self.last = self.n**2 - 1

    def __repr__(self):
        res = ""
        for j in range(self.n):
            for i in range(self.n):
                number = self.board[(i,j)]
                if number != self.last:
                    res += "%s" % (number + 1)
                else:
                    res += ' '
            res += "\n"
        return res


    def possible_moves(self):
        res = [] 
        gap = None
        for j in  range(self.n):
            for i in range(self.n):
                    if self.board[(i,j)] == self.last:
                        gap = (i,j)
                        break
            if gap is not None:
                break
        assert gap != None

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
                if number != j*self.n + i and (number != self.last and i == self.n -1 and j == self.n -1):
                    return False
        return True


    def swap(self, a, b):
        self.board[a], self.board[b] = self.board[b], self.board[a]


if __name__ == "__main__":
    b = Board(3)
    print b
    print b.check_if_finished()
    b.swap((2, 1), (2, 2))
    print b
    print b.possible_moves()
    print b.check_if_finished()

