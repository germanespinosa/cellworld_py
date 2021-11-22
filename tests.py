from cellworld_py import *
import matplotlib as mpl
import numpy as np
import time

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
    assert (str(Transformation_list(n=4, size=1, rotation=0)) == "[{\"size\":1.0,\"rotation\":0.0},{\"size\":1.0,\"rotation\":90.0},{\"size\":1.0,\"rotation\":180.0},{\"size\":1.0,\"rotation\":270.0}]")
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
    w = World.get_from_parameters_names("hexagonal", "canonical", "10_05")
    print("ok")
    occlusions = w.cells.where("occluded", True)
    print (occlusions)


def test_display():
    print("testing display: ", end="")
    wc = World_configuration.get_from_name("hexagonal")
    src_space = Space(center=Location(0, 0), shape=Shape(6), transformation=Transformation(1, 30))
    r = (21.0 + 1.0 / 3.0)
    wi = World_implementation.create(wc, space=src_space, cell_transformation=Transformation(size=1.15470053837925/r, rotation=0), relative_locations_transformations=Transformation_list(n=6, rotation=-90, size=1/r))
    from matplotlib import pyplot as plt
    o = Cell_group_builder.get_from_name("hexagonal", "10_08", "occlusions")
    w = World.get_from_parameters(wc, wi, o)
    d = Display(w, show_axes=True)
    plt.show()
    print("ok")


def test_experiment():
    print("testing experiment: ", end="")
    e = Experiment.get_from_file("test_trajectory.json")
    wc = World_configuration.get_from_name("hexagonal")
    src_space = Space(center=Location(0.5, 0.5), shape=Shape(6), transformation=Transformation(1, 30))
    r = (21.0 + 1.0 / 3.0)
    wi = World_implementation.create(wc, space=src_space, cell_transformation=Transformation(size=1.15470053837925/r, rotation=0), relative_locations_transformations=Transformation_list(n=6, rotation=-90, size=1/r))
    from matplotlib import pyplot as plt
    o = Cell_group_builder.get_from_name("hexagonal", "10_05", "occlusions")
    w = World.get_from_parameters(wc, wi, o)
    d = Display(w, show_axes=True, background_color="black", cell_edge_color="white", habitat_edge_color="white")
    # for epi in e.episodes:
    max_vel = 0
    for episode in e.episodes:
        unique_steps = episode.trajectories.get_agent_trajectory("human").get_unique_steps()
        human_velocity = unique_steps.get_filtered_velocities(.9)["human"]
        max_vel = max(human_velocity + [max_vel])
        vel_color_index = [v/max(human_velocity) for v in human_velocity]
        cmap = plt.cm.jet(vel_color_index)
        d.add_trajectories(unique_steps, {"human": cmap})

    cmap = plt.cm.jet
    norm = mpl.colors.Normalize(vmin=0, vmax=2)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ticks=np.linspace(0, 2, 50), boundaries=np.arange(-0.05, 2.1, .1))
    cbar.ax.set_yticklabels([])

    plt.show()

def test_velocities():
    v = Velocities()
    v.append(1.0)
    v.append(2.0)
    v.append(5.0)
    v.append(1000.0)
    fv = v.complementary_filter(.9)
    print(fv)
    assert (fv[0] == 1.0)
    assert (fv[1] == 1.1)
    assert (fv[2] == 1.49)
    rv = fv.outliers_filter(.3)
    print(rv)


def test_message_router():
    class routing_test:
        def __init__(self, i):
            self.i = i
            pass

        def handler_1(self, m):
            return self.i, 1

        def handler_2(self, m):
            return self.i, 2

    rt1 = routing_test(1)
    rt2 = routing_test(2)
    mr = Message_router()
    mr.add_route("1$", rt1.handler_1)
    mr.add_route("2$", rt2.handler_2)
    assert (mr.route(Message("test1", "route 1")) == [(1, 1)])
    assert (mr.route(Message("test2", "route 2")) == [(2, 2)])


def test_message_queue():
    ml = Message_list()
    assert (len(ml) == 0)
    ml.queue(Message("a", "a"))
    assert (len(ml) == 1)
    ml.queue(Message("a", "b"))
    assert (len(ml) == 2)
    m = ml.dequeue()
    assert (m.header == "a" and m.body == "a")
    assert (len(ml) == 1)
    m = ml.dequeue()
    assert (m.header == "a" and m.body == "b")
    assert (len(ml) == 0)


unrouted_counter = 0
responses_counter = 0

def test_message_server(m):
    class routing_test:
        def __init__(self, i):
            self.i = i
            self.h1 = 0
            self.h2 = 0
            self.handled = []
            pass

        def handler_1(self, m):
            self.h1 += 1
            self.handled.append(m.body)
            return self.i, 1

        def handler_2(self, m):
            self.h2 += 1
            self.handled.append(m.body)
            return Message("response", 2)

    def unrouted(message):
        global unrouted_counter
        unrouted_counter += 1

    def response(message):
        global responses_counter
        responses_counter += 1

    global unrouted_counter
    global responses_counter

    unrouted_counter = 0
    responses_counter = 0

    rt1 = routing_test(1)
    rt2 = routing_test(2)

    ms = Message_server()
    ms.router.unrouted_message = unrouted
    ms.router.add_route("1$", rt1.handler_1)
    ms.router.add_route("2$", rt2.handler_2)
    ms.start(5000)
    mc = Message_client("127.0.0.1", 5000)
    mc.router.unrouted_message = response
    mc.start()
    for i in range(m * 2):
        mc.connection.send(Message("test%i" % ((i % 2) + 1), str(i)))
    p = 0
    while rt1.h1 + rt1.h2 + rt2.h1 + rt2.h2 + unrouted_counter < m * 2:
        pass

    while responses_counter < m:
        pass

    mc.stop()
    mc.connection.close()
    ms.stop()
    assert(rt1.h1 == m)
    assert(rt1.h2 == 0)
    assert(rt2.h1 == 0)
    assert(rt2.h2 == m)
    assert(unrouted_counter == 0)

def test_message_client(m):
    class routing_test:
        def __init__(self, i):
            self.i = i
            self.h1 = 0
            self.h2 = 0
            self.handled = []
            pass

        def handler_1(self, m):
            self.h1 += 1
            self.handled.append(m.body)

        def handler_2(self, m):
            self.h2 += 1
            self.handled.append(m.body)

    def unrouted(message):
        global unrouted_counter
        unrouted_counter += 1

    global unrouted_counter
    global responses_counter

    unrouted_counter = 0
    responses_counter = 0

    rt1 = routing_test(1)
    rt2 = routing_test(2)

    ms = Message_server()
    ms.router.unrouted_message = unrouted
    ms.router.add_route("1$", rt1.handler_1)
    ms.router.add_route("2$", rt2.handler_2)
    ms.start(5000)
    for i in range(m * 2):
        mc = Message_client("127.0.0.1", 5000)
        mc.connection.send(Message("test%i" % ((i % 2) + 1), str(i)))
        mc.connection.close()

    p = 0
    while rt1.h1 + rt1.h2 + rt2.h1 + rt2.h2 + unrouted_counter < m * 2:
        pass

    ms.stop()
    assert(rt1.h1 == m)
    assert(rt1.h2 == 0)
    assert(rt2.h1 == 0)
    assert(rt2.h2 == m)
    assert(unrouted_counter == 0)



# test_coordinates()
# test_coordinates_list()
# test_location()
# test_location_list()
# test_shape()
# test_transformation()
# test_space()
# test_cell()
# test_world_configuration()
# test_world_implementation()
# test_world()
# test_display()
# test_experiment()
# test_velocities()
# test_message_router()
#test_message_queue()
[test_message_server(20) for i in range(10)]
[test_message_client(20) for i in range(10)]
#print (version())
#
# while Time_out(5):
#     print(1)
#     time.sleep(1)
