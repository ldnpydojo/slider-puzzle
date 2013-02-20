import copy
from sets import Set

def build_grid(n):
    g = []
    count = 1
    for i in range(0, n):
        g.append([])
        for j in range(0, n):
            g[i].append(count)
            count += 1

    g[n-1][n-1] = 0

    # We use tuples so we can save the grids in a hash - so we know if we've seen this grid before
    result = []
    for r in g:
        result.append(tuple(r))
    return tuple(result)


def print_grid(g):
    for l in g:
        print l
    print


def match_level(g, level):
    """ Have we matched the first 'level' tiles with the answer grid """
    for i in range(len(g)):
        for j in range(len(g[i])):
            level -= 1
            if g[i][j] != finished_grid[i][j]:
                return False
            # Special case - when doing the last row we must put 2 tiles in place each time
            elif i == len(g) - 2 and g[i+1][j] != finished_grid[i+1][j]:
                return False
            elif level == 0:
                return True


def get_banned_moves(g, level):
    """ When a tile is in place dont F* with it """
    result = []
    size = len(g)

    for i in range(len(g)):
        for j in range(len(g[i])):
            if level == 0:
                break
            result.append((i, j))
            level -= 1

    # If we have to move the last element of the row in place then dont ban the move
    # in the top left or it will be impossible
    if len(result) % size == size - 1:
        result.pop()

    return result


def duplicate_tuple(g, x1, y1, x2, y2):
    result = []
    for i in range(len(g)):
        r = []
        for j in range(len(g[i])):
            if i == x1 and j == y1:
                r.append(g[x2][y2])
            elif i == x2 and j == y2:
                r.append(g[x1][y1])
            else:
                r.append(g[i][j])
        result.append(tuple(r))
    return tuple(result)


def find_zero(g):
    for i in range(len(g)):
        for j in range(len(g[i])):
            if g[i][j] == 0:
                return (i, j)
    raise Exception('no 0')


def legal_moves(g):
    result = []
    size = len(g) - 1
    zx, zy = find_zero(g)

    if zx > 0 and (zx-1, zy) not in banned_moves:
        new_g = duplicate_tuple(g, zx, zy, zx-1, zy)
        result.append(new_g)
    if zx < size and (zx+1, zy) not in banned_moves:
        new_g = duplicate_tuple(g, zx, zy, zx+1, zy)
        result.append(new_g)
    if zy > 0 and (zx, zy-1) not in banned_moves:
        new_g = duplicate_tuple(g, zx, zy-1, zx, zy)
        result.append(new_g)
    if zy < size and (zx, zy+1) not in banned_moves:
        new_g = duplicate_tuple(g, zx, zy+1, zx, zy)
        result.append(new_g)

    return result


def bf_search(grid, level):
    """ Use bf_search or df_search not both """
    states_we_have_seen_before = Set(grid)
    current_states = [grid]
    result = None
    counter = 0

    while result is None:
        next_states = Set()

        for g in current_states:
            for gg in legal_moves(g):
                if gg not in states_we_have_seen_before:
                    states_we_have_seen_before.add(gg)
                    next_states.add(gg)

        for t in next_states:
            if match_level(t, level):
                result = t
                break

        current_states = next_states
        counter += 1

    return (counter, result)


def df_search(grid, level):
    """ Use bf_search or df_search not both """
    states_we_have_seen_before = Set(grid)

    def recur(inner_grid, itter, level):
        counter = 0
        next_states = Set()

        for gg in legal_moves(inner_grid):
            if gg not in states_we_have_seen_before:
                states_we_have_seen_before.add(gg)
                next_states.add(gg)

        for t in next_states:
            if match_level(t, level):
                return (size * size * size - itter, t)

        if itter > 0:
            for t in next_states:
                r = recur(t, itter - 1, level)
                if r:
                    return r
        return None

    return recur(grid, size * size * size, level)


# Sample random grids:
#gr = ((4,6,0), (5,2,3), (1,7,8))
#gr = ((8,0,5), (1,7,2), (6,4,3))
#gr = ((5,1,8,2), (14,13,12,4), (6,9,0,10), (3,7,11,15))
gr = ((10,5,1,3), (7,11,2,12), (13,9,8,4), (6,15,0,14))

size = len(gr)
finished_grid = build_grid(size)

print 'Starting grid:'
print_grid(gr)

for i in range(1, size * size - size + 1):
    banned_moves = get_banned_moves(gr, i - 1)
    counter, gr = bf_search(gr, i)
    #counter, gr = df_search(gr, i)
    print 'Move ' + str(i) + ' into place. In ' + str(counter) + ' moves'
    print_grid(gr)
