import re

import parsing
import config

USAGE = config.get('command_prefix') + "tell <nick> <message>"

def execute(**kwargs):
    match_object = re.match(r"([^\s]+)[\s]+([^\s]+)", kwargs['arguments'])
    if match_object:
        nick = match_object.group(1)
        message = match_object.group(2)
        parsing.ActionTrigger(
            run_once=True,
            regex=r".*PRIVMSG %s :%s.*",
            action=lambda: connection.send_to_channel(kwargs['channel'], nick + " said: " + message)
        )
    else:
        connection.send_to_channel(channel, USAGE)
