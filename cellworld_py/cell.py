from .util import *
from .location import Location
from .coordinates import Coordinates, Coordinates_list


class Cell(Json_object):
    def __init__(self, cell_id=0, coordinates=Coordinates(), location=Location(), occluded=False):
        check_type(coordinates, Coordinates, "wrong type for coordinates")
        check_type(location, Location, "wrong type for location")
        check_type(cell_id, int, "wrong type for cell_id")
        check_type(occluded, bool, "wrong type for occluded")
        self.id = int(cell_id)
        self.coordinates = coordinates
        self.location = location
        self.occluded = occluded


class Cell_group_builder(Json_list):
    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=int)

    def get_from_name(world_name, name, *argv):
        if not type(world_name) is str:
            raise "incorrect type for world_name"
        if not type(name) is str:
            raise "incorrect type for name"
        return Json_get(get_resource("cell_group", world_name, name, *argv), Cell_group_builder)



class Cell_group:
    def __init__(self, world, cell_group_builder=[]):
        self.world = world
        self.cell_ids = cell_group_builder.cell_ids

    def add(self, cell):
        if cell.id in self.cell_ids:
            return False
        self.cell_ids.append(cell.id)
        return True

    def __str__(self):
        cgb = Cell_group_builder()
        cgb.cell_ids = self.cell_ids
        return str(cgb.cell_ids)


class Cell_map:

    def __init__(self, coordinates_list):
        check_type(coordinates_list, Coordinates_list, "incorrect type for coordinates_list")
        self.coordinates = coordinates_list
        x = self.coordinates.get_x()
        y = self.coordinates.get_x()
        self.base_x = min(x)
        self.base_y = min(y)
        size_x = max(x) - self.base_x + 1
        size_y = max(y) - self.base_y + 1
        self.index = [[-1 for y in range(size_y)] for x in range(size_x)]
        for i, c in enumerate(coordinates_list.coordinates):
            self.index[c.x][c.y] = i

    def __getitem__(self, coordinates):
        check_type(coordinates, Coordinates, "incorrect type for coordinates")
        return self.index[coordinates.x][coordinates.y]

