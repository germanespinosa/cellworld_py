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

    def atan(self, loc):
        v = loc-self
        return math.atan2(v.x, v.y)

    def dist(self, loc):
        v = loc-self
        return (v.x ** 2 + v.y ** 2) ** .5


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
