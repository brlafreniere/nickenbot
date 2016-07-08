import string
import socket
import time
import datetime
import re
import sys

import config
import command
import parsing

BUFSIZE = 512

COMMANDS = {
    'NICKSERV_IDENTIFY': "PRIVMSG NickServ IDENTIFY %s %s",
}

class ServerConnection:
    def __init__(self, **kwargs):
        self.registered = False

        print("Creating new IRC connection.")
        print("YAML Configuration:")
        config.display()

        self.message_interpreter = parsing.MessageInterpreter(self)
        self.create_socket()
        self.start_loop()

    def identify_with_nickserv(self):
        self.send_message(
            COMMANDS['NICKSERV_IDENTIFY'] % (config.get("nick"), config.get("password"))
        )

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((config.get('server'), config.get('port')))
        time.sleep(1)

    def join_config_channels(self):
        for channel in config.get("channels"):
            self.join_channel(channel)

    def join_channel(self, channel):
        self.send_message("JOIN " + channel)

    def send_to_channel(self, channel, message):
        self.send_message("PRIVMSG %s %s" % (channel, message))

    def send_message(self, message, log=True):
        if log:
            log_messages(message)
        self.sock.send(message + "\r\n")

    def pong(self, message):
        ping_id = re.match(r"PING (.*)", message).group(1)
        self.send_message("PONG " + ping_id, False)

    def receive_messages(self):
        raw = self.sock.recv(BUFSIZE)

        messages = filter(None, raw.split("\r\n"))

        log_messages(messages, True)

        return messages

    def register_nick_and_username(self):
        self.send_message(string.join([
            "NICK",
            config.get("nick")], " "
        ))

        self.send_message(string.join([
            "USER",
            config.get("nick"),
            socket.gethostname(),
            config.get("server"),
            config.get("nick")], " "
        ))


    def start_loop(self):
        while True:
            self.message_interpreter.process_messages(self.receive_messages())

            if not self.registered:
                self.register_nick_and_username()
                self.registered = True

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

