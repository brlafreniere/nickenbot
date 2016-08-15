import re

from .. import config, irc
from ..parsing import Action, MessageInterpreter

USAGE = config.get('command_prefix') + "tell <nick> <message>"

def execute(**kwargs):
    # extract bot command + arguments:
    bot_command_mo = re.match(r"([\w]+)[\s]+(.*)", kwargs['arguments'])

    if bot_command_mo:
        nick = bot_command_mo.group(1)
        message = bot_command_mo.group(2)

        # ':blaine!blaine@Clk-E28261F1 PRIVMSG #test :#tell'
        action = Action(
            run_once=True,
            regex=r"^:%s![^\s]+ PRIVMSG %s :.*" % (nick, kwargs['channel']),
            action=lambda match: irc.send_to_channel(kwargs['channel'], kwargs['caller_nick'] + " said: " + message)
        )
        irc.send_to_channel(kwargs['channel'], "Ok, I will tell %s the next time I see them." % nick)
        MessageInterpreter.action_insertion_queue.append(action)
    else:
        irc.send_to_channel(kwargs['channel'], USAGE)
