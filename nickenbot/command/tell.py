import re

import nickenbot.parsing
import nickenbot.config
import nickenbot.connection

USAGE = nickenbot.config.get('command_prefix') + "tell <nick> <message>"

connection = nickenbot.connection.ServerConnection()

def execute(**kwargs):
    match_object = re.match(r"([^\s]+)[\s]+([^\s]+)", kwargs['arguments'])
    if match_object:
        nick = match_object.group(1)
        message = match_object.group(2)
        # ':blaine!blaine@Clk-E28261F1 PRIVMSG #test :#tell'
        nickenbot.parsing.ActionTrigger(
            run_once=True,
            regex=r":%s.*@.* PRIVMSG %s :.*" % (nick, kwargs['channel']),
            action=lambda match: connection.send_to_channel(kwargs['channel'], kwargs['caller_nick'] + " said: " + message)
        )
    else:
        connection.send_to_channel(channel, USAGE)
