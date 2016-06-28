import socket
import time
import re

import config

BUFSIZE = 512

class Connection:
    def __init__(self, **kwargs):
        print("Creating new IRC connection with the following configuration:")
        print(open('config.yaml', 'r').read())

        self.connect()

        self.send_message("NICK " + config.get('nick'))
        self.send_message("USER " + config.get('nick') + " ")

        for channel in config.get('channels'):
            self.join_channel(channel)

        while True:
            data = self.sock.recv(BUFSIZE)
            if data:
                self.parse_data(data)

    def parse_data(self, data):
        messages = data.split("\r\n")

        for message in messages:
            if message:
                print(" [R] <-  " + repr(message))

                if re.match(r"^PING .*", message):
                    self.pong(message)
                

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((config.get('server'), config.get('port')))
        time.sleep(1)

    def join_channel(self, channel):
        self.send_message("JOIN " + channel)

    def send_message(self, message):
        print(" [S]  -> " + repr(message))
        self.sock.send(message + "\r\n")

    def pong(self, message):
        ping_id = re.match(r"PING (.*)", message).group(1)
        self.send_message("PONG " + ping_id)
