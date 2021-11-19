import socket
from threading import Thread
from .util import Message, check_type
from .message_connection import Message_connection
from .message_router import Message_router


class Message_client:
    def __init__(self, ip, port):
        self.unrouted_messages = None
        self.failed_messages = None
        self.running = False
        self.registered = False
        self.router = Message_router()
        self.parameters = (ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.parameters)
        self.connection = Message_connection(s, self.failed_messages)
        self.thread = None

    def start(self):
        self.running = True
        self.thread = Thread(target=self.__proc__)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join(4)

    def disconnect(self):
        pass

    def __proc__(self):
        while self.running and self.connection.active():
            message = self.connection.receive()
            if message:
                responses = self.router.route(message)
                if responses:
                    for response in responses:
                        if isinstance(response, Message):
                            self.connection.send(response)
