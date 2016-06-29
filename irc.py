import string
import socket
import time
import datetime
import re
import sys

import config

BUFSIZE = 512

class Connection:
    def identify_with_nickserv(self):
        self.send_message("PRIVMSG NickServ IDENTIFY %s %s" % (config.get("nick"), config.get("password")))

    def parse_messages(self, messages):
        for message in messages:
            if re.match(r"^PING .*", message):
                self.pong(message)
                break
            if re.search(r".*001 %s.*" % config.get("nick"), message):
                self.join_config_channels()
                break
            if re.match(r".*NOTICE.*nickname.*registered.*", message):
                self.identify_with_nickserv()
                break
            if not self.registered:
                self.register_nick_and_username()
                self.registered = True

                
    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((config.get('server'), config.get('port')))
        time.sleep(1)

    def log_messages(self, messages, received=False):
        if type(messages) is str:
            messages = [messages]

        for message in messages:
            log_message = []
            if received:
                log_message.append(" [RECEIVED] - ")
            else:
                log_message.append(" [SENT]     - ")
            log_message.append(datetime.datetime.now().isoformat())
            log_message.append(": ")
            log_message.append(message)
            print(string.join(log_message))

    def join_config_channels(self):
        for channel in config.get("channels"):
            self.join_channel(channel)

    def join_channel(self, channel):
        self.send_message("JOIN " + channel)

    def send_message(self, message):
        self.log_messages(message)
        self.sock.send(message + "\r\n")

    def pong(self, message):
        ping_id = re.match(r"PING (.*)", message).group(1)
        self.send_message("PONG " + ping_id)

    def receive_messages(self):
        raw = self.sock.recv(BUFSIZE)

        messages = filter(None, raw.split("\r\n"))

        self.log_messages(messages, True)

        return messages

    def receive_all(self):
        messages = self.receive_messages()
        self.parse_messages(messages)
        while messages:
            messages = self.receive_messages()
            self.parse_messages(messages)

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
            self.parse_messages(self.receive_all())

    def __init__(self, **kwargs):
        print("Creating new IRC connection. YAML Configuration:")
        print(open('config.yaml', 'r').read() + "\n")

        self.registered = False

        self.create_socket()

        self.start_loop()
