from .util import *
from .coordinates import *
from .location import *

# https://doc-0g-c0-docs.googleusercontent.com/docs/securesc/p1k2kcnbi5084m8mcvkl0g9hv0spbipl/qm0siiabkdslf53ec2jokfp3kr8ak43p/1635330750000/09425701396282971692/17330557302626681944Z/1e8IRExVcKgw2trIn6Lj_Dm080Ky21T7s?e=download


class Step(Json_object):
    def __init__(self, time_stamp=0.0, agent_name="", frame=0, coordinates=Coordinates(0,0), location=Location(0,0)):
        self.time_stamp = time_stamp
        self.agent_name = agent_name
        self.frame = frame
        self.coordinates = coordinates
        self.location = location


class Velocities(Json_list):
    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=float)

    def complementary_filter(self, a): # complementary filter
        check_type(a, float, "wrong type for a")
        if a <= 0 or a >= 1:
            raise ArithmeticError("filter parameter should be > 0 and < 1")
        filtered = Velocities()
        last = self[0]
        for v in self:
            nv = (a * last + (1 - a) * v)
            last = nv
            filtered.append(nv)
        return filtered

    def outliers_filter(self, a):
        check_type(a, float, "wrong type for a")
        if a <= 0:
            raise ArithmeticError("filter parameter should be > 0")
        filtered = Velocities()
        last = self[0]
        next_good = False
        for v in self:
            if next_good or abs(v-last)/last <= a:
                next_good = False
                filtered.append(v)
            else:
                next_good = True
            last = v
        return filtered



class Trajectories(Json_list):
    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=Step)

    def get_velocities(self):
        velocities = {}
        last_locations = {}
        last_time_stamp = {}
        for s in self:
            if s.agent_name not in velocities:
                velocities[s.agent_name] = Velocities(allowedType=float)
                velocities[s.agent_name].append(0.0)
            else:
                time_dif = s.time_stamp - last_time_stamp[s.agent_name]
                velocity = s.location.dist(last_locations[s.agent_name]) / time_dif
                velocities[s.agent_name].append(velocity)
            last_locations[s.agent_name] = s.location
            last_time_stamp[s.agent_name] = s.time_stamp
        return velocities

    def get_filtered_velocities(self, complementary=None, outliers=None):
        avs = self.get_velocities()
        for agent_name in avs:
            if complementary:
                avs[agent_name] = avs[agent_name].complementary_filter(complementary)
            if outliers:
                avs[agent_name] = avs[agent_name].outliers_filter(outliers)
        return avs

    def get_unique_steps(self):
        unique_steps = Trajectories()
        last_locations = {}
        for s in self:
            if s.agent_name not in last_locations or not last_locations[s.agent_name] == s.location:
                unique_steps.append(s)
            last_locations[s.agent_name] = s.location
        return unique_steps


    def get_agent_names(self):
        agent_names = []
        for s in self:
            if s.agent_name not in agent_names:
                agent_names.append(s.agent_name)
        return agent_names

    def get_agent_trajectory(self, agent_name):
        return self.where("agent_name", agent_name)


class Episode(Json_object):
    def __init__(self, start_time="", time_stamp=0.0, end_time="", trajectories=Trajectories()):
        self.start_time = start_time
        self.time_stamp = time_stamp
        self.end_time = end_time
        self.trajectories = trajectories


class Episode_list(Json_list):
    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=Episode)


class Experiment(Json_object):
    def __init__(self, name="", world_name="", subject_name="", duration=0.0, start_time="", episodes=Episode_list()):
        self.name = name
        self.world_name = world_name
        self.subject_name = subject_name
        self.duration = duration
        self.start_time = start_time
        self.episodes = episodes

    @staticmethod
    def get_from_file(file_name):
        e = Json_get(open(file_name).read(), Experiment)
        check_type(e, Experiment, "")
        return e

    @staticmethod
    def get_from_url(url):
        e = Json_get(get_web_json(resource_uri=url), Experiment)
        check_type(e, Experiment, "")
        return e


