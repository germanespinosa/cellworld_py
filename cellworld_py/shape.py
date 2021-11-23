from .location import Location, Location_list
from .util import *
import math


class Shape(Json_object):
    def __init__(self, sides=6):
        self.sides = int(sides)


class Transformation(Json_object):
    def __init__(self, size=0, rotation=0):
        self.size = float(size)
        self.rotation = float(rotation)


class Transformation_list(Json_list):
    def __init__(self, iterable=None, n=None, size=0.0, rotation=0.0):
        Json_list.__init__(self, iterable, allowedType=Transformation)
        if n:
            for a in range(n):
                self.append(Transformation(float(size), float(rotation) + float(a) * (360.0 / float(n))))


class Space(Json_object):
    def __init__(self, center=Location(), shape=Shape(), transformation=Transformation()):
        check_type(center, Location, "incorrect type for center")
        check_type(shape, Shape, "incorrect type for shape")
        check_type(transformation, Transformation, "incorrect type for transformation")
        self.center = center
        self.shape = shape
        self.transformation = transformation


    @staticmethod
    def transform_to(location, src_space, dst_space):
        check_type(location, Location, "incorrect type for location")
        check_type(src_space, Space, "incorrect type for src_space")
        check_type(dst_space, Space, "incorrect type for dst_space")
        size_ratio = dst_space.transformation.size / src_space.transformation.size
        rotation = math.radians(dst_space.transformation.rotation - src_space.transformation.rotation)
        dist = src_space.center.dist(location)
        theta = src_space.center.atan(location)
        new_location = Location(dst_space.center.x, dst_space.center.y)
        return new_location.move(theta + rotation, dist * size_ratio)



class Polygon:

    def __init__(self, center, sides=0, radius=1.0, rotation=0, vertices=None):
        if vertices is None:
            vertices = Location_list()
        check_type(center, Location, "incorrect type for center")
        check_type(sides, int, "incorrect type for sides")
        check_type(vertices, Location_list, "incorrect type for sides")
        self.center = center
        self.vertices = vertices
        self.radius = float(radius)
        if sides > 0:
            if len(self.vertices.locations) != 0:
                raise "cannot use sides and vertices together"
            rotation = float(rotation)
            if sides == 0:
                raise "incorrect parameters"
            theta = math.radians(rotation)
            inc = 2.0 * math.pi / sides
            for s in range(sides):
                c = center
                self.vertices.append(c.move(theta, radius))
                theta += inc
        else:
            if len(self.vertices) == 0:
                raise "must specify either sides or vertices"

    def move(self, location=None, theta=None, dist=None):
        check_type(location, Location, "incorrect type for location")
        dif = Location(0, 0)
        if location is None:
            if theta is None or dist is None:
                raise "incorrect parameters"
            dif.move(theta, dist)
        else:
            dif = location - self.center
        self.center = location
        for v in self.vertices:
            v = v + dif

    def is_between(self, src=None, dst=None, theta=None, dist=None):
        check_type(src, Location, "incorrect type for src")
        if dst is not None:
            check_type(dst, Location, "incorrect type for dst")
            theta = src.atan(dst)
            dist = src.dist(dst)
        else:
            if theta is None or dist is None:
                raise "either dst or theta and dist should be used"
        dist_center = src.dist(self.center)
        theta_center = src.atan(self.center)
        diff_theta_center, direction_center = angle_difference(theta, theta_center)
        if dist < dist_center - self.radius:
            return False
        for v in self.vertices:
            vertex_distance = src.dist(v)
            if vertex_distance < dist:
                theta_vertex = src.atan(v)
                diff_theta_vertex, direction_vertex = angle_difference(theta, theta_vertex);
                if direction_center == -direction_vertex:
                    if diff_theta_center + diff_theta_vertex < math.pi:
                        return True
        return False



class Polygon_list(Json_list):

    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=Polygon)
