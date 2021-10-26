from cellworld_py import *


def test_coordinates():
    print("testing coordinates: ", end="")
    assert (Coordinates(1, 2).x == Coordinates(1, 3).x)
    assert (Coordinates(1, 2).y == Coordinates(3, 2).y)
    assert (Coordinates(1, 2) + Coordinates(3, 4) == Coordinates(4, 6))
    assert ('{"x":1,"y":2}' == str(Coordinates(1, 2)))
    assert ('{"x":1,"y":2}' == str(Coordinates(1, 2)))
    assert (Json_get({"x": 1, "y": 2}, Coordinates) == Coordinates(1, 2))
    print("ok")


def test_coordinates_list():
    print("testing coordinates list: ", end="")
    cl = Coordinates_list()
    try:
        cl.append(1)
        raise "failed to check type"
    except:
        pass
    cl.append(Coordinates(1, 2))
    assert (str(cl) == "[{\"x\":1,\"y\":2}]")
    cl = Json_get("[{\"x\":1,\"y\":2},{\"x\":3,\"y\":4},{\"x\":5,\"y\":6},{\"x\":7,\"y\":8}]", Coordinates_list)
    assert (len(cl) == 4)
    assert (str(cl[0]) == "{\"x\":1,\"y\":2}")
    assert (str(cl[1]) == "{\"x\":3,\"y\":4}")
    assert (str(cl[2]) == "{\"x\":5,\"y\":6}")
    assert (str(cl[3]) == "{\"x\":7,\"y\":8}")
    assert (str(cl) == "[{\"x\":1,\"y\":2},{\"x\":3,\"y\":4},{\"x\":5,\"y\":6},{\"x\":7,\"y\":8}]")
    assert (cl.get("x") == [1, 3, 5, 7])
    assert (cl.get("y") == [2, 4, 6, 8])
    print("ok")


def test_location():
    print("testing location: ", end="")
    assert (Location(1, 2).x == Location(1, 3).x)
    assert (Location(1, 2).y == Location(3, 2).y)
    assert (Location(1, 2) + Location(3, 4) == Location(4, 6))
    assert ('{"x":1.0,"y":2.0}' == str(Location(1, 2)))
    assert ('{"x":1.0,"y":2.0}' == str(Location(1, 2)))
    assert (Json_get({"x": 1, "y": 2}, Location) == Location(1, 2))
    assert (Location(1, 1).move(0, 1) == Location(1, 2))
    print("ok")


def test_location_list():
    print("testing location list: ", end="")
    cl = Location_list()
    try:
        cl.append(1)
        raise "failed to check type"
    except:
        pass
    cl.append(Location(1, 2))
    assert (str(cl) == "[{\"x\":1.0,\"y\":2.0}]")
    cl = Json_get("[{\"x\":1,\"y\":2},{\"x\":3,\"y\":4},{\"x\":5,\"y\":6},{\"x\":7,\"y\":8}]", Location_list)
    assert (len(cl) == 4)
    assert (str(cl[0]) == "{\"x\":1.0,\"y\":2.0}")
    assert (str(cl[1]) == "{\"x\":3.0,\"y\":4.0}")
    assert (str(cl[2]) == "{\"x\":5.0,\"y\":6.0}")
    assert (str(cl[3]) == "{\"x\":7.0,\"y\":8.0}")
    assert (str(cl) == "[{\"x\":1.0,\"y\":2.0},{\"x\":3.0,\"y\":4.0},{\"x\":5.0,\"y\":6.0},{\"x\":7.0,\"y\":8.0}]")
    assert (cl.get("x") == [1, 3, 5, 7])
    assert (cl.get("y") == [2, 4, 6, 8])
    print("ok")


def test_shape():
    print("testing shape: ", end="")
    assert (Shape(1).sides == 1)
    assert (Shape(5).sides == 5)
    assert (Json_get("{\"sides\":6}", Shape) == Shape(6))
    assert (str(Shape(6)) == "{\"sides\":6}")
    print("ok")


def test_transformation():
    print("testing transformation: ", end="")
    assert (Transformation(1.0, 2.0).size == 1.0)
    assert (Transformation(1.0, 2.0).rotation == 2.0)
    assert (Json_get("{\"size\":1.0,\"rotation\":2.0}", Transformation) == Transformation(1.0, 2.0))
    assert (str(Transformation(1.0, 2.0)) == "{\"size\":1.0,\"rotation\":2.0}")
    assert (str(Transformation.get_transformations(4,0,1)) == "[{\"size\":1.0,\"rotation\":0.0},{\"size\":1.0,\"rotation\":90.0},{\"size\":1.0,\"rotation\":180.0},{\"size\":1.0,\"rotation\":270.0}]")
    print("ok")


def test_space():
    print("testing space: ", end="")
    assert (Space(Location(1, 2), Shape(6), Transformation(0, 1)).center == Location(1, 2))
    assert (Space(Location(1, 2), Shape(6), Transformation(0, 1)).shape == Shape(6))
    assert (Space(Location(1, 2), Shape(6), Transformation(0, 1)).transformation == Transformation(0, 1))
    assert (str(Space(Location(1, 2), Shape(6), Transformation(0, 1))) == '{"center":{"x":1.0,"y":2.0},"shape":{"sides":6},"transformation":{"size":0.0,"rotation":1.0}}')
    assert (Json_get('{"center":{"x":1.0,"y":2.0},"shape":{"sides":6},"transformation":{"size":0.0,"rotation":1.0}}',Space) == Space(Location(1, 2), Shape(6), Transformation(0, 1)))
    print("ok")



def test_cell():
    print("testing cell: ", end="")
    assert (Cell(1, Coordinates(1, 2), Location(3, 4), True).id == 1)
    assert (Cell(1, Coordinates(1, 2), Location(3, 4), True).coordinates == Coordinates(1, 2))
    assert (Cell(1, Coordinates(1, 2), Location(3, 4), True).location == Location(3, 4))
    assert (Cell(1, Coordinates(1, 2), Location(3, 4), True).occluded == True)
    assert (str(Cell(1, Coordinates(1, 2), Location(3, 4), True)) == '{"id":1,"coordinates":{"x":1,"y":2},"location":{"x":3.0,"y":4.0},"occluded":true}')
    assert (Json_get('{"id":1,"coordinates":{"x":1,"y":2},"location":{"x":3.0,"y":4.0},"occluded":true}',Cell) == Cell(1, Coordinates(1, 2), Location(3, 4), True))
    print("ok")


def test_world_configuration():
    print("testing world_configuration: ", end="")
    wc = World_configuration.get_from_name("hexagonal")
    assert(wc.cell_shape.sides == 6)
    assert(len(wc.cell_coordinates) == 331)
    assert(len(wc.connection_pattern) == 6)
    print("ok")


def test_world_implementation():
    print("testing world_implementation: ", end="")
    wi = World_implementation.get_from_name("hexagonal", "canonical")
    check_type(wi, World_implementation, "wrong type for World_implementation")
    assert (len(wi.cell_locations) == 331)
    check_type(wi.space, Space, "wrong type for space")
    check_type(wi.cell_transformation, Transformation, "wrong type for cell_transformation")
    print("ok")

def test_world():
    print("testing world: ", end="")
    w = World.get_from_parameters_names("hexagonal", "canonical")
    w = World.get_from_parameters_names("hexagonal", "canonical")
    w = World.get_from_parameters_names("hexagonal", "canonical", "00_00")
    print("ok")

def test_display():
    wc = World_configuration.get_from_name("hexagonal")
    src_space = Space(center=Location(0, 0), shape=Shape(6), transformation=Transformation(21.0 + 1.0 / 3.0, 30))
    wi = World_implementation.create(wc, space=src_space, cell_transformation=Transformation(size=1, rotation=0), relative_locations_transformations=(6, -90, 1))
    from matplotlib import pyplot as plt
    print("testing display: ", end="")
    o = Cell_group_builder.get_from_name("hexagonal", "00_00", "occlusions")
    w = World.get_from_parameters(wc, wi, o)
    d = Display(w)
    plt.show()
    print("ok")


test_coordinates()
test_coordinates_list()
test_location()
test_location_list()
test_shape()
test_transformation()
test_space()
test_cell()
test_world_configuration()
test_world_implementation()
test_world()
test_display()
