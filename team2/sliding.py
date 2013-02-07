import pprint

class Board:

    def __init__(self, n):
        self.n = n
        self.board = dict(((i,j),j*n+i+1) for i in range(n) for j in range(n))
        self.board[(n-1,n-1)] = ' '

    def __repr__(self):
        res = ""
        for j in range(self.n):
            for i in range(self.n):
                res += "%s"%self.board[(i,j)]
            res += "\n"
        return res


    def possible_moves(self):
        res = []
        gap = None
        for i in  range(self.n):
            for j in range(self.n):
                    if self.board[(i,j)] == ' ':
                        gap = (i,j)
                        break
            if gap is not None:
                break
        assert gap != None

        (i,j) = gap
        if i >= 1:
            res.append((i-1, j))
        if i < self.n:
            res.append((i+1, j))
        if j >= 1:
            res.append((i, j-1))
        if j < self.n:
            res.append((i, j+1))
        assert len(res) > 0

        return res


    def swap(self, a, b):#a pos ' ' b posn chosen square slidng
        self.board[a], self.board[b] = self.board[b], self.board[a]

if __name__ == "__main__":
    b = Board(3)
    print b
    print b.possible_moves()

