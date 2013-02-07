from slider import *


def test_check_ordered_slider():
    check_slider(ordered_slider(3))

if __name__ == '__main__':
    print_slider(ordered_slider(3))
    print_slider(random_slider(3))
