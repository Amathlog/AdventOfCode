from pathlib import Path
import os
import math

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

x_range, y_range = entries[0].split(",")
x_range = [int(x) for x in x_range.split("..")]
y_range = [int(y) for y in y_range.split("..")]

def get_x(x_0: int, steps: int) -> int:
    if steps == 0:
        return 0

    if steps > x_0:
        steps = x_0

    return (steps) * x_0 - ((steps - 1) * (steps)) // 2

def get_peak_y(y_0) -> int:
    if y_0 < 0:
        return 0
    return get_x(y_0, y_0)


def get_y(y_0, steps: int) -> int:
    if steps == 0:
        return 0

    if steps <= y_0:
        return get_x(y_0, steps)

    peak_y = get_peak_y(y_0)
    if y_0 > 0:
        steps -= y_0
        y_0 = 0
    return peak_y - get_x(y_0, steps)

def will_hit_y(y_0, y_range):
    peak_y = get_peak_y(y_0)
    offset = 0
    if y_0 > 0:
        offset = y_0
        y_0 = 0
    
    b = (y_0 + 0.5)
    n_min = -(-b - math.sqrt(b ** 2 + 2 * (peak_y - y_range[1])))
    n_max = -(-b - math.sqrt(b ** 2 + 2 * (peak_y - y_range[0])))

    res = set()
    if int(n_min) == n_min:
        res.add(int(n_min) + offset)
    if int(n_max) == n_max:
        res.add(int(n_max) + offset)
    if int(n_min) != int(n_max):
        res.update(range(int(n_min) + 1 + offset, int(n_max) + 1 + offset))

    return tuple(res)

def will_hit_x(x_0, x_range):
    x_peak = get_x(x_0, x_0)
    if x_peak < x_range[0]:
        return tuple(), False

    infinite = x_peak <= x_range[1]
    max_x = x_range[1]
    if infinite:
        max_x = x_peak

    b = (x_0 + 0.5)
    n_min = -(-b + math.sqrt(b ** 2 - 2 * x_range[0]))
    n_max = -(-b + math.sqrt(b ** 2 - 2 * max_x))
    
    res = set()
    if int(n_min) == n_min:
        res.add(int(n_min))
    if int(n_max) == n_max:
        res.add(int(n_max))
    if int(n_min) != int(n_max):
        res.update(range(int(n_min) + 1, int(n_max) + 1))

    return tuple(res), infinite
    
if __name__ == "__main__":
    max_y = 0
    velocities = []
    for x in range(1, x_range[1] + 1):
        for y in range(300, y_range[0]-1, -1):
            x_hit, infinite = will_hit_x(x, x_range)
            y_hit = will_hit_y(y, y_range)

            if len(x_hit) == 0 or len(y_hit) == 0:
                continue

            hit = set(x_hit).intersection(y_hit)
            if len(hit) > 0 or (infinite and (x_hit[-1] in set(y_hit) or x_hit[-1] <= y_hit[0])):
                velocities.append((x,y))
                peak_y = get_peak_y(y)
                if peak_y > max_y:
                    max_y = peak_y
                continue

    print("First answer:", max_y)
    print("Second answer:", len(velocities))