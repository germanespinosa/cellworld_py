import math
import requests
import json
global cellworld_data_base_uri
from datetime import datetime, timedelta

cellworld_data_base_uri = "https://raw.githubusercontent.com/germanespinosa/cellworld_data/master/"

def get_resource(resource_type, key0, *argv):
    resource_uri = cellworld_data_base_uri + resource_type + "/" + key0
    for arg in argv:
        resource_uri += "." + arg
    response = requests.get(resource_uri)
    return json.loads(response.text)


def get_web_json(resource_uri):
    response = requests.get(resource_uri)
    return json.loads(response.text)


class Time_out:
    def __init__(self, seconds=1.0):
        self.end_time = datetime.now() + timedelta(seconds=seconds)

    def __bool__(self):
        return self.end_time > datetime.now()

class Timer:
    def __init__(self, seconds=0):
        self.time = seconds
        self.check_point = datetime.now()

    def to_seconds(self):
        delta=datetime.now() - self.check_point
        return delta.seconds

    def __bool__(self):
        return self.to_seconds() < self.time

    def time_out(self):
        return self.to_seconds() > self.time


def check_type(v, t, m):
    if not isinstance(v, t):
        raise TypeError(m)


def check_types(v, ts, m):
    r = False
    for t in ts:
        if isinstance(v, t):
            r = True
    if not r:
        raise TypeError(m)


def normalize(angle):
    check_type(angle, float, "wrong type for angle")
    while angle < 0:
        angle += 2.0 * math.pi
    while angle > 2 * math.pi:
        angle -= 2.0 * math.pi
    return angle;


def angle_difference(a1, a2):
    a1 = normalize(a1)
    a2 = normalize(a2)
    if a1 > a2:
        dif = a1 - a2;
        if dif < math.pi:
            return dif, 1;
        else:
            return a2 + math.pi * 2.0 - a1, -1
    else:
        dif = a2 - a1;
        if dif < math.pi:
            return dif, -1
        else:
            return a1 + math.pi * 2.0 - a2, 1


def angle_between(value, lim1, lim2, inclusive=False):
    diff1, dir1 = angle_difference(value, lim1)
    diff2, dir2 = angle_difference(value, lim2)
    if inclusive:
        if diff1 == 0 or diff2 == 0:
            return True
    return (dir1 + dir2) == 0


class Json_object:

    def __str__(self):
        s = ""
        v = vars(self)
        for k in v:
            if k[0] == "_":
                continue
            if s:
                s += ","
            s += "\"%s\":" % k
            if isinstance(v[k], str):
                s += "%s" % json.dumps(v[k])
            elif isinstance(v[k], bool):
                s += "%s" % str(v[k]).lower()
            else:
                s += "%s" % str(v[k])
        return "{%s}" % s

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        v = vars(self)
        vo = vars(other)
        for k in v:
            if k[0] == "_":
                continue
            if v[k] != vo[k]:
                return False
        return True

    def copy(self):
        return Json_get(str(self),type(self))

    def format(self, format_string):
        check_type(format_string, str, "wrong type for format_string")
        v = vars(self)
        for k in v:
            if not isinstance(v[k], Json_object):
                continue
            pos = format_string.find("{"+k+":")
            if pos >= 0:
                sub_format_start = format_string.find(":", pos) + 1
                sub_format_end = sub_format_start
                bracket_count = 1
                while bracket_count and sub_format_end < len(format_string):
                    c = format_string[sub_format_end]
                    if c == '{':
                        bracket_count += 1
                    if c == '}':
                        bracket_count -= 1
                    sub_format_end +=1
                sub_format = format_string[sub_format_start:sub_format_end-1]
                sub_str = v[k].format(sub_format)
                format_string = format_string[:pos] + sub_str + format_string[sub_format_end:]
        return format_string.format(**vars(self))


class Json_list(list):

    def __init__(self, iterable=None, allowedType=None):
        iterable = list() if not iterable else iterable
        iter(iterable)
        self._allowedType = allowedType
        map(self._typeCheck, iterable)
        list.__init__(self, iterable)

    def allowedType(self):
        return self._allowedType

    def _typeCheck(self, val):
        if not self._allowedType:
            return
        if not isinstance(val, self._allowedType):
            raise TypeError("Wrong type %s, this list can hold only instances of %s" % (type(val),
                                                                                        str(self._allowedTypes)))

    def __iadd__(self, other):
        map(self._typeCheck, other)
        list.__iadd__(self, other)
        return self

    def __add__(self, other):
        iterable = [item for item in self] + [item for item in other]
        return Json_list(iterable, self._allowedType)

    def __radd__(self, other):
        iterable = [item for item in other] + [item for item in self]
        if isinstance(other, Json_list):
            return self.__class__(iterable, other.allowedType())
        return Json_list(iterable, self._allowedType)

    def __setitem__(self, key, value):
        itervalue = (value,)
        if isinstance(key, slice):
            iter(value)
            itervalue = value
        map(self._typeCheck, itervalue)
        list.__setitem__(self, key, value)

    def __setslice__(self, i, j, iterable):
        iter(iterable)
        map(self._typeCheck, iterable)
        list.__setslice__(self, i, j, iterable)

    def append(self, val):
        self._typeCheck(val)
        list.append(self, val)

    def extend(self, iterable):
        iter(iterable)
        map(self._typeCheck, iterable)
        list.extend(self, iterable)

    def insert(self, i, val):
        self._typeCheck(val)
        list.insert(self, i, val)

    def __str__(self):
        return "[" + ",".join([str(x) for x in self]) + "]"

    def get(self, m):
        it = type(vars(self._allowedType())[m])
        l = Json_list(allowedType=it)
        for i in self:
            l.append(vars(i)[m])
        return l

    def where(self, m, v, o="=="):
        nl = type(self)()
        for i in self:
            if type(vars(i)[m]) is str or issubclass(type(vars(i)[m]), Json_object):
                e = "'%s' %s '%s'" % (str(vars(i)[m]), o, str(v))
            else:
                e = "%s %s %s" % (str(vars(i)[m]), o, str(v))
            if eval(e):
                nl.append(i)
        return nl


def Json_get(j, t):
    if isinstance(j, str):
        j = json.loads(j)
    if issubclass(t, Json_object):
        check_type(j, dict, "wrong type for j")
        v = t()
        for k in j:
            it = type(getattr(v, k))
            if issubclass(it, Json_object):
                av = Json_get(j[k], it)
            elif issubclass(it, Json_list):
                av = Json_get(j[k], it)
            else:
                av = it(j[k])
            setattr(v, k, av)
        return v
    elif issubclass(t, Json_list):
        check_type(j, list, "wrong type for j")
        l = t()
        it = l.allowedType()
        ic = it().__class__
        for i in j:
            if issubclass(ic, Json_object) or issubclass(ic, Json_list):
                l.append(Json_get(i, it))
            else:
                l.append(i)
        return l
    else:
        raise TypeError("wrong type for t")


class Message(Json_object):
    def __init__(self, header="", body=""):
        self.header = header
        self.body = str(body)

    def get_body(self, t):
        return Json_get(self.body, t)

    def set_body(self, v):
        self.body = str(v)


class Message_list(Json_list):
    def __init__(self, iterable=None):
        Json_list.__init__(self, iterable, allowedType=Message)

    def queue(self, message):
        check_type(message, Message, "wrong type for message")
        self.append(message)

    def dequeue(self):
        if len(self):
            message = self[0]
            del self[0]
            return message
        return None

    def contains(self, header):
        for message in self:
            if message.header == header:
                return True
        return False

    def get_message(self, header):
        for i in range(len(self)):
            if self[i].header == header:
                message = self[i]
                del self[i]
                return message
        return None

    def get_last_message(self, header):
        message = None
        for i in range(len(self)):
            if self[i].header == header:
                message = self[i]
                del self[i]
        return message
