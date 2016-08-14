COMMANDS = {
    'NICKSERV_IDENTIFY': "PRIVMSG NickServ IDENTIFY %s %s",
}

def identify_with_nickserv(servconn):
    servconn.send_message(
        COMMANDS['NICKSERV_IDENTIFY'] % (config.get("nick"), config.get("password"))
    )

def join_config_channels(servconn):
    for channel in config.get("channels"):
        servconn.join_channel(channel)

def join_channel(servconn, channel):
    servconn.send_message("JOIN " + channel)

def send_to_channel(servconn, channel, message):
    servconn.send_message("PRIVMSG %s %s" % (channel, message))

def pong(servconn, message):
    ping_id = re.match(r"PING (.*)", message).group(1)
    servconn.send_message("PONG " + ping_id, False)

def register_nick_and_username(servconn):
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
