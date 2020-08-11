"""
Given two 2D polygons write a function that calculates the IoU of their areas,
defined as the area of their intersection divided by the area of their union.
The vertices of the polygons are constrained to lie on the unit circle and you
can assume that each polygon has at least 3 vertices, given and in sorted order.

- You are free to use basic math functions/libraries (sin, cos, atan2, numpy etc)
  but not geometry-specific libraries (such as shapely).
- You are free to look up geometry-related formulas, optionally copy paste in
  short code snippets and adapt them to your needs.
- We do care and evaluate your general code quality, structure and readability
  but you do not have to go crazy on docstrings.
"""
import math


def iou(polygon1, polygon2):
    # Remove duplicate points in a polygon
    polygon1 = remove_duplicate(polygon1)
    polygon2 = remove_duplicate(polygon2)

    # Find lines with consecutive points for each polygon
    line_poly1 = make_lined_polygon(polygon1)
    line_poly2 = make_lined_polygon(polygon2)

    # Find all points on intersecting polygon
    poly = find_polygon_intersections(line_poly1, line_poly2)
    poly = remove_duplicate(poly)

    # Reorder points of polygon
    poly = reorder_polygon(poly)

    # Calculate areas of each of the polygons
    intersection = area_poly(poly)
    area1 = area_poly(polygon1)
    area2 = area_poly(polygon2)
    union = area1 + area2 - intersection
    return intersection / union


def round_it(number):
    """Round each of the numbers to 10 significant digits to keep python from running into floating point issues"""
    return round(number, 10)


def remove_duplicate(polygon):
    """Remove all the duplicates vertices from a polygon and return the rest of vertices"""
    duplicateless = []
    for i in polygon:
        i = (round_it(i[0]), round_it(i[1]))
        if i in duplicateless:
            pass
        else:
            duplicateless.append(i)
    return duplicateless


def find_line(point1, point2):
    """Calculate a,b,c for the line given two points where the line of the form ax+by=c"""
    a = point2[1] - point1[1]
    b = point1[0] - point2[0]
    c = a * point1[0] + b * point1[1]
    c = round_it(c)
    return (a, b, c)


def intersection_of_lines(line1, line2):
    """Calculates the intersection point of 2 lines and returns the point of Intersection"""
    A1 = line1[0]
    B1 = line1[1]
    C1 = line1[2]
    A2 = line2[0]
    B2 = line2[1]
    C2 = line2[2]
    Det = A1 * B2 - A2 * B1
    Det = round_it(Det)
    if Det == 0:
        if round_it(C1 * A2) == round_it(C2 * A1) and round_it(C1 * B2) == round_it(C2 * B1):
            # Same Line
            return "same"
        else:
            # Parallel Non intersecting
            return "No Point"
    else:
        x = (B2 * C1 - B1 * C2) / Det
        y = (A1 * C2 - A2 * C1) / Det
        x = round_it(x)
        y = round_it(y)
        return (x, y)


def make_lined_polygon(poly):
    """Given a polygon by consecutive vertices, the function return the lines connecting the vertices"""
    line_array = []
    for i in range(len(poly)):
        point0 = poly[i - 1]
        point1 = poly[i]
        line = find_line(point0, point1)
        line_array.append((point0, point1, line))
    return line_array


def check_point_between_points(point, point1, point2):
    """Checks if a point is part of the line segment formed by point1 and point2"""
    x = point[0]
    y = point[1]
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    x_diff = (x - x1) * (x2 - x)
    y_diff = (y - y1) * (y2 - y)
    if x_diff >= 0 and y_diff >= 0:
        return True
    else:
        return False


def find_polygon_intersections(line_poly1, line_poly2):
    """Given 2 polygons, the function checks intersections between lines of different polygons
    and adds it to the intersecting polygon vertices if the vertex is part of the line segments"""
    intersecting_polygon = []
    for i in line_poly1:
        for j in line_poly2:
            line1 = i[2]
            line2 = j[2]
            intersection = intersection_of_lines(line1, line2)
            if intersection == "No Point":
                pass
            elif intersection == "same":
                intersecting_polygon.append(i[0])
                intersecting_polygon.append(i[1])
            else:
                check1 = check_point_between_points(intersection, i[0], i[1])
                check2 = check_point_between_points(intersection, j[0], j[1])
                if check1 and check2:
                    intersecting_polygon.append(intersection)
    return intersecting_polygon


def reorder_polygon(poly):
    """Reorders the vertices in a cyclic order by sorting on the arctan of the vertex w.r.t. the center"""
    count = len(poly)
    if count == 0:
        return []
    center_x = 0
    center_y = 0
    for i in poly:
        center_x += i[0]
        center_y += i[1]
    center_x = center_x / count
    center_y = center_y / count
    ordered_poly = sorted(poly, key=lambda point: math.atan2(point[1] - center_x, point[0] - center_y))
    return ordered_poly


def area_poly(poly):
    """Calculates the area of the polygon using the cross product rule"""
    area = 0
    n = len(poly)
    if n <= 2:
        return 0
    for i in range(n):
        x = poly[(i + 1) % n][0]
        y = poly[(i + 2) % n][1] - poly[i][1]
        area += x * y
    return abs(area / 2)


if __name__ == "__main__":

    cases = []
    # Case 1: a vanilla case (see https://imgur.com/a/dSKXHPF for a diagram)
    poly1 = [
        (-0.7071067811865475, 0.7071067811865476),
        (0.30901699437494723, -0.9510565162951536),
        (0.5877852522924729, -0.8090169943749476),
    ]
    poly2 = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (0.7071067811865475, -0.7071067811865477),
    ]
    cases.append((poly1, poly2, "simple case", 0.12421351279682288))
    # Case 2: another simple case
    poly1 = [
        (1, 0),
        (0, 1),
        (-0.7071067811865476, -0.7071067811865476),
    ]
    poly2 = [
        (-0.1736481776669303, 0.984807753012208),
        (-1, 0),
        (0, -1),
    ]
    cases.append((poly1, poly2, "simple case 2", 0.1881047657147776))
    # Case 3: yet another simple case, note the duplicated point
    poly1 = [
        (0, -1),
        (-1, 0),
        (-1, 0),
        (0, 1),
    ]
    poly2 = [
        (0.7071067811865476, 0.7071067811865476),
        (-0.7071067811865476, 0.7071067811865476),
        (-0.7071067811865476, -0.7071067811865476),
        (0.7071067811865476, -0.7071067811865476),
        (0.7071067811865476, -0.7071067811865476),
    ]
    cases.append((poly1, poly2, "simple case 3", 0.38148713966109243))

    # Case 4: shared edge
    poly1 = [
        (-1, 0),
        (-0.7071067811865476, -0.7071067811865476),
        (0.7071067811865476, -0.7071067811865476),
        (1, 0),
    ]
    poly2 = [
        (0, 1),
        (-1, 0),
        (1, 0),
    ]
    cases.append((poly1, poly2, "shared edge", 0.0))

    # Case 5: same polygon
    poly1 = [
        (0, -1),
        (-1, 0),
        (1, 0),
    ]
    poly2 = [
        (0, -1),
        (-1, 0),
        (1, 0),
    ]
    cases.append((poly1, poly2, "same same", 1.0))

    # Case 6: polygons do not intersect
    poly1 = [
        (-0.7071067811865476, 0.7071067811865476),
        (-1, 0),
        (-0.7071067811865476, -0.7071067811865476),
    ]
    poly2 = [
        (0.7071067811865476, 0.7071067811865476),
        (1, 0),
        (0.7071067811865476, -0.7071067811865476),
    ]
    cases.append((poly1, poly2, "no intersection", 0.0))

    import time

    t0 = time.time()

    for poly1, poly2, description, expected in cases:
        computed = iou(poly1, poly2)
        print('-' * 20)
        print(description)
        print("computed:", computed)
        print("expected:", expected)
        print("PASS" if abs(computed - expected) < 1e-8 else "FAIL")

    # details here don't matter too much, but this shouldn't be seconds
    dt = (time.time() - t0) * 1000
    print("done in %.4fms" % dt)
