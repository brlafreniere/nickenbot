import string
import socket
import time
import datetime
import re
import sys

import config
import command

def log_messages(messages, received=False):
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

BUFSIZE = 512

COMMANDS = {
    'NICKSERV_IDENTIFY': "PRIVMSG NickServ IDENTIFY %s %s",
}

PARSE_REGEX = {
    'BOT_COMMAND': r".*PRIVMSG ([^\s]+) :%s([\w]+)[\s]*(.*)",
    'PING': r"^PING .*",
    'RPL_WELCOME': r"001 %s",
    'NICK_REGISTERED': r"NOTICE.*nickname.*registered",
}

class ServerConnection:
    def identify_with_nickserv(self):
        self.send_message(
            COMMANDS['NICKSERV_IDENTIFY'] % (config.get("nick"), config.get("password"))
        )

    def parse_messages(self, messages):
        for message in messages:
            result = re.match(PARSE_REGEX['BOT_COMMAND'] % config.get("command_prefix"), message)
            if result:
                command.execute(result.group(1), result.group(2), result.group(3), self)
                break
            #if command.register.check(message):
                #command.register.trigger(message)
                #break
            if re.match(PARSE_REGEX['PING'], message):
                self.pong(message)
                break
            if re.search(PARSE_REGEX['RPL_WELCOME'] % config.get("nick"), message):
                self.join_config_channels()
                break
            if re.search(PARSE_REGEX['NICK_REGISTERED'], message):
                self.identify_with_nickserv()
                break
            if not self.registered:
                self.register_nick_and_username()
                self.registered = True
                
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

    def send_message(self, message):
        log_messages(message)
        self.sock.send(message + "\r\n")

    def pong(self, message):
        ping_id = re.match(r"PING (.*)", message).group(1)
        self.send_message("PONG " + ping_id)

    def receive_messages(self):
        raw = self.sock.recv(BUFSIZE)

        messages = filter(None, raw.split("\r\n"))

        log_messages(messages, True)

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
