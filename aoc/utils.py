import itertools

def neighboor_iter(x: int, y: int, limit_x: int, limit_y: int, discard_center: bool = True, discard_diagonal: bool = False):
    inner_range = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)) if discard_diagonal else itertools.product((-1, 0, 1), (-1, 0, 1))
    for incr_x, incr_y in inner_range:
        if incr_x == 0 and incr_y == 0 and discard_center:
            continue

        x_ = x + incr_x
        y_ = y + incr_y

        if x_ < 0 or x_ >= limit_x or y_ < 0 or y_ >= limit_y:
            continue

        yield x_, y_

