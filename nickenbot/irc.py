COMMANDS = {
    'NICKSERV_IDENTIFY': "PRIVMSG NickServ IDENTIFY %s %s",
}

    def identify_with_nickserv(self):
        self.send_message(
            COMMANDS['NICKSERV_IDENTIFY'] % (config.get("nick"), config.get("password"))
        )

    def join_config_channels(self):
        for channel in config.get("channels"):
            self.join_channel(channel)

    def join_channel(self, channel):
        self.send_message("JOIN " + channel)

    def send_to_channel(self, channel, message):
        self.send_message("PRIVMSG %s %s" % (channel, message))

    def pong(self, message):
        ping_id = re.match(r"PING (.*)", message).group(1)
        self.send_message("PONG " + ping_id, False)

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

