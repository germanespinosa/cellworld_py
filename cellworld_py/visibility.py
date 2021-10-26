from .location import Location, Locations_list
from .shape import Polygon, Polygon_list
from .util import *


class Location_visibility:

    def __init__(self, occlusions):
        check_type(occlusions, Polygon_list, "incorrect type for occlusions")
        self.occlusions = occlusions

    def is_visible(self, src, dst):
        check_type(src, Location, "incorrect type for src")
        check_type(dst, Location, "incorrect type for dst")
        theta = src.atan(dst)
        dist = src.dist(dst)
        for occlusion in self.occlusions.polygons:
            if occlusion.is_between(src, theta=theta, dist=dist):
                return False
        return True
