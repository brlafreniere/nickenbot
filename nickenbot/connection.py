import string
import socket
import time
import datetime
import re
import sys

from config import ConfigManager

BUFSIZE = 512

class ServerConnection:
    instance = None

    def __init__(self, **kwargs):
        if not ServerConnection.instance:
            ConfigManager.network = kwargs['network']
            self.registered = False
            self.create_socket()
            ServerConnection.instance = self
        else:
            return ServerConnection.instance

    @classmethod
    def get(klass):
        if klass.instance:
            return klass.instance
        else:
            return ServerConnection()

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ConfigManager.get('server'), ConfigManager.get('port')))
        time.sleep(1)

    def send_message(self, message, log=True):
        if log:
            log_messages(message)
        self.sock.send(message + "\r\n")

    def receive_messages(self):
        raw = self.sock.recv(BUFSIZE)

        messages = filter(None, raw.split("\r\n"))

        log_messages(messages, True)

        return messages

def log_messages(messages, received=False):
    if type(messages) is str:
        messages = [messages]

    # filter out PING messages
    messages = filter(lambda message: not re.match(r"^PING.*", message), messages)

    for message in messages:
        log_message = []
        if received:
            log_message.append(" [RECEIVED] - ")
        else:
            log_message.append(" [SENT]     - ")
        log_message.append(datetime.datetime.now().isoformat())
        log_message.append(" - ")
        log_message.append(repr(message))
        print(string.join(log_message))

