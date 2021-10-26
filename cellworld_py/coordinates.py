from .util import *

class Coordinates(Json_object):
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, o):
        c = Coordinates()
        c.x = self.x + o.x
        c.y = self.y + o.y
        return c


class Coordinates_list (Json_list):
    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=Coordinates)

    def get_x(self):
        x = []
        for coordinates in self:
            x.append(coordinates.x)
        return x

    def get_y(self):
        y = []
        for coordinates in self:
            y.append(coordinates.y)
        return y

