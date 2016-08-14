import re
import string
import socket

import config
import connection

servconn = connection.ServerConnection.connections[0]

COMMANDS = {
    'NICKSERV_IDENTIFY': "PRIVMSG NickServ IDENTIFY %s %s",
}

def identify_with_nickserv():
    servconn.send_message(
        COMMANDS['NICKSERV_IDENTIFY'] % (config.get("nick"), config.get("password"))
    )

def join_config_channels():
    for channel in config.get("channels"):
        join_channel(channel)

def join_channel(channel):
    servconn.send_message("JOIN " + channel)

def send_to_channel(channel, message):
    servconn.send_message("PRIVMSG %s %s" % (channel, message))

def pong(message):
    ping_id = re.match(r"PING (.*)", message).group(1)
    servconn.send_message("PONG " + ping_id, False)

def register_nick_and_username():
    servconn.send_message(string.join([
        "NICK",
        config.get("nick")], " "
    ))

    servconn.send_message(string.join([
        "USER",
        config.get("nick"),
        socket.gethostname(),
        config.get("server"),
        config.get("nick")], " "
    ))
