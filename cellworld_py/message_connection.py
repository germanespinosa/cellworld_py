from .util import check_type, Message, Message_list, Json_get
import socket


class Message_connection:

    def __init__(self, s, failed_message=None):
        check_type(s, socket.socket, "incorrect type for s")
        self.socket = s
        self.socket.settimeout(1)
        self.failed_message = failed_message
        self.pending_messages = Message_list()
        self.is_active = True

    def close(self):
        self.is_active = False
        self.socket.close()

    def active(self):
        if not self.is_active:
            return False
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = self.socket.recv(16, socket.MSG_PEEK)
        except socket.timeout:
            return True
        except:
            self.is_active = False
            return False  # socket was closed for some other reason
        return True

    def send(self, message):
        check_type(message, Message, "incorrect type for message")
        message_str = str(message)
        print("sending:", message_str)
        message_bytes = message_str.encode()
        message_bytes += b'\x00'
        self.socket.send(message_bytes)

    def receive(self):
        if not self.is_active:
            return
        data = bytes()
        try:
            data = self.socket.recv(8192)
        except socket.timeout as e:
            pass
        except Exception as e:
            self.is_active = False
        else:
            if data:
                messages_str = data.decode().split('\x00')
                for message_str in messages_str:
                    if message_str:
                        try:
                            message = Json_get(message_str, Message)
                            self.pending_messages.queue(message)
                        except:
                            if self.failed_message:
                                self.failed_message(message_str)
        return self.pending_messages.dequeue()
