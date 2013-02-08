import random

def generate_grid(size):
    numbers = range(size * size)
    return [numbers[i*size:i*size+size] for i in range(size)]


def shuffle_grid(grid, n):
    size = len(grid)
    zx, zy = (0, 0)
    for i in range(n):
        possible = []
        if zx > 0:
            possible.append((zx-1, zy))
        if zy > 0:
            possible.append((zx, zy-1))
        if zx < size-1:
            possible.append((zx+1, zy))
        if zy < size-1:
            possible.append((zx, zy+1))
        nx, ny = random.choice(possible)

        grid[nx][ny], grid[zx][zy] = grid[zx][zy], grid[nx][ny]

        zx, zy = nx, ny


def print_possible(grid):
    for line in grid:
        for element in line:
            if element:
                print "% 3d" % element,
            else:
                print '   ',
        print


def solved(grid):
    ## DIRTY BUT IT WORKS
    return str(grid) == str(generate_grid(len(grid)))

    ## HEART IN THE RIGHT PLACE
    grid = tuple(map(tuple, grid))
    return grid == sorted(map(sorted, grid))

    ## LEARNED C IN UNI
    size = len(grid)
    expected_value = 0
    solved = False
    for row in range(size):
        for element in range(size):
            if element == expected_value:
                solved = True
                expected_value = expected_value + 1
            else:
                solved = False
    return solved

def basics(g):
    print_possible(g)
    print solved(g)
    shuffle_grid(g, 10)
    print_possible(g)
    print solved(g)

def shuffle_l(g):
    pass

def find(grid, n):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == n:
                return (i, j)
    raise Exception

find_zero = lambda grid: find(grid, 0)


def solve(grid):
    # PLAN B
    # return generate_grid(len(grid))

    for i in xrange(10000000):
        zx, zy = find_zero(grid)
        switchable = [grid[zx+1][zy] if zx < len(grid)-1 else None,
                      grid[zx-1][zy] if zx > 0 else None,
                      grid[zx][zy+1] if zy < len(grid)-1 else None,
                      grid[zx][zy-1] if zy > 0 else None]

        switchable = filter(lambda n: n is not None, switchable)
        the_switchee = random.choice(switchable)
        sx, sy = find(grid, the_switchee)
        grid[sx][sy], grid[zx][zy] = grid[zx][zy], grid[sx][sy]

        if solved(grid):
            return grid

    raise CouldNotSolveGridException()


class CouldNotSolveGridException(Exception):
    pass




g = generate_grid(10)
shuffle_grid(g, 10)
print_possible(g)
print
print_possible(solve(g))


#basics(g)
