from .util import *
import math


class Location(Json_object):

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, o):
        c = Location()
        c.x = self.x + o.x
        c.y = self.y + o.y
        return c

    def __sub__(self, o):
        c = Location()
        c.x = self.x - o.x
        c.y = self.y - o.y
        return c

    def move(self, theta, dist):
        self.x += math.sin(theta) * dist
        self.y += math.cos(theta) * dist
        return self

    def atan(self, location):
        check_type(location, Location, "incorrect type for location")
        v = location-self
        return math.atan2(v.x, v.y)

    def dist(self, location=None, segment=None):
        if location:
            check_type(location, Location, "incorrect type for location")
            v = location-self
            return (v.x ** 2 + v.y ** 2) ** .5
        elif segment:
            check_type(segment, tuple, "incorrect type for segment")
            line_start, line_end = segment
            check_type(line_start, Location, "incorrect type for line_start")
            check_type(line_end, Location, "incorrect type for line_end")
            normal_length = line_end.dist(line_start)
            distance = ((self.x - line_start.x) * (line_end.y - line_start.y) - (self.y - line_start.y) * (line_end.x - line_start.x)) / normal_length
            return abs(distance)


class Location_list(Json_list):

    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=Location)

    def get_x(self):
        x = []
        for location in self:
            x.append(location.x)
        return x

    def get_y(self):
        y = []
        for location in self:
            y.append(location.y)
        return y


def segments_intersect(segment1, segment2):
    check_type(segment1, tuple, "incorrect type for segment1")
    check_type(segment2, tuple, "incorrect type for segment2")
    segment1_point1, segment1_point2 = segment1
    segment2_point1, segment2_point2 = segment2
    check_type(segment1_point1, Location, "incorrect type for segment1_point1")
    check_type(segment1_point2, Location, "incorrect type for segment1_point2")
    check_type(segment2_point1, Location, "incorrect type for segment2_point1")
    check_type(segment2_point2, Location, "incorrect type for segment2_point2")
    t1 = segment1_point1.atan(segment1_point2)
    t11 = segment1_point1.atan(segment2_point1)
    t12 = segment1_point1.atan(segment2_point2)
    if not angle_between(t1, t11, t12):
        return False
    t2 = segment2_point1.atan(segment2_point2)
    t21 = segment2_point1.atan(segment1_point1)
    t22 = segment2_point1.atan(segment1_point2)
    if not angle_between(t2, t21, t22):
        return False
    return True
