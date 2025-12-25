import copy
import math
from typing import List, Tuple
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.point import Point2D, intersect_seg

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def is_on_segment(seg: Tuple[Point2D, Point2D], p: Point2D) -> bool:
    min_x = min(seg[0].x, seg[1].x)
    max_x = max(seg[0].x, seg[1].x)
    min_y = min(seg[0].y, seg[1].y)
    max_y = max(seg[0].y, seg[1].y)

    if min_x == max_x:
        return p.x == min_x and min_y <= p.y <= max_y
    else:
        return p.y == min_y and min_x <= p.x <= max_x
    
def is_inside_polygon(polygon: List[Tuple[Point2D, Point2D]], p: Point2D):
    # First check if it is on any segment of the polygon
    for seg in polygon:
        if is_on_segment(seg, p):
            return True
        
    # Then if not, do the sum of all the angles between the point and the segements extremity.
    # If the point is inside, the sum should be 2Pi

    resulting_angle = 0
    for seg in polygon:
        p0_dir = seg[0] - p
        p1_dir = seg[1] - p

        cross = p0_dir.cross_2D(p1_dir)
        dot = p0_dir.dot(p1_dir)

        resulting_angle += math.atan2(cross, dot)

    return math.isclose(abs(resulting_angle), 2 * math.pi, abs_tol=1e-2)


def is_rect_inside_polygon(polygon: List[Tuple[Point2D, Point2D]], t1: Point2D, t2: Point2D):
    t3 = Point2D(t1.x, t2.y)
    t4 = Point2D(t2.x, t1.y)

    if not is_inside_polygon(polygon, t3) or not is_inside_polygon(polygon, t4):
        return False

    # When we have validated that all the corners are in the polygon, validate that the segments don't have intersections with the polygon
    for seg in [(t1, t3), (t3, t2), (t2, t4), (t4, t1)]:
        for edge in polygon:
            # Discard edges that are part of the segment
            intersects, _, t, t_ = intersect_seg(*seg, *edge)
            if intersects and 0 < t < 1 and 0 < t_ < 1:
                return False
        
    return True

@profile
def solve(entry: List[str]) -> int:
    vertices = [Point2D(*map(int, e.split(","))) for e in entry]
    polygon = [(vertices[i], vertices[(i+1)%len(vertices)]) for i in range(len(vertices))]

    min_x, min_y, max_x, max_y = 0, 0, 0, 0

    tiles_with_area = []
    for i, tile1 in enumerate(vertices[:-1]):
        min_x = min(min_x, tile1.x)
        min_y = min(min_y, tile1.y)
        max_x = max(max_x, tile1.x)
        max_y = max(max_y, tile1.y)

        for tile2 in vertices[i+1:]:
            diff = tile2 - tile1
            area = (abs(diff.x) + 1) * (abs(diff.y) + 1)
            tiles_with_area.append((tile1, tile2, area))

    vertices.append(vertices[0])

    tiles_with_area.sort(key=lambda x: x[2], reverse=True)

    part_1 = tiles_with_area[0][2]

    for t1, t2, area in tiles_with_area:
        if is_rect_inside_polygon(polygon, t1, t2):
            break

    part_2 = (t1, t2, area)
    
    return part_1, part_2


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
