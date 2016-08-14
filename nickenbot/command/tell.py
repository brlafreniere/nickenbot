import re

from .. import parsing, config, connection, irc


USAGE = config.get('command_prefix') + "tell <nick> <message>"

def execute(**kwargs):
    match_object = re.match(r"([^\s]+)[\s]+([^\s]+)", kwargs['arguments'])
    if match_object:
        nick = match_object.group(1)
        message = match_object.group(2)
        # ':blaine!blaine@Clk-E28261F1 PRIVMSG #test :#tell'
        parsing.ActionTrigger(
            run_once=True,
            regex=r":%s.*@.* PRIVMSG %s :.*" % (nick, kwargs['channel']),
            action=lambda match: irc.send_to_channel(kwargs['channel'], kwargs['caller_nick'] + " said: " + message)
        )
    else:
        irc.send_to_channel(kwargs['channel'], USAGE)
