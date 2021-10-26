import math

import requests
import json

global cellworld_data_base_uri
cellworld_data_base_uri = "https://raw.githubusercontent.com/germanespinosa/cellworld_data/master/"


def get_resource(resource_type, key0, *argv ):
    resource_uri = cellworld_data_base_uri + resource_type + "/" + key0
    for arg in argv:
        resource_uri += "." + arg
    response = requests.get(resource_uri)
    return json.loads(response.text)


def check_type(v, t, m):
    if not isinstance(v, t):
        raise m


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


class Json_object:
    def __init__(self):
        pass

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
                s += "\"%s\"" % v[k]
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
