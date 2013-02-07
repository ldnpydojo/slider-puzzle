from slider import *


def test_check_ordered_board():
    check_board(ordered_board(3))

if __name__ == '__main__':
    print_board(ordered_board(3))
    print_board(random_board(3))
