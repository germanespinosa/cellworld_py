import types
from .util import check_type, check_types, Message, Json_get
import re


class Message_router:
    def __init__(self):
        self.routes = {}
        self.failed_message = None
        self.unrouted_message = None
        self.processing = False

    def add_route(self, pattern, handler, body_type=None):
        check_type(pattern, str, "incorrect type for pattern")
        check_types(handler, [types.FunctionType, types.MethodType], "incorrect type for handler")
        self.routes[pattern] = (handler, body_type)

    def route(self, message):
        responses = []
        check_type(message, Message, "incorrect type for message")
        for pattern in self.routes.keys():
            if re.search(pattern, message.header):
                (handler, body_type) = self.routes[pattern]
                if body_type:
                    responses.append(handler(message.get_body(body_type)))
                else:
                    responses.append(handler(message))
        if not responses:
            if self.unrouted_message:
                self.unrouted_message(message)
        return responses