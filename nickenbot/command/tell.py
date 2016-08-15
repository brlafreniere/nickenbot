import re

from .. import irc
from ..config import ConfigManager
from ..parsing import Action, MessageInterpreter

USAGE = ConfigManager.get('command_prefix') + "tell <nick> <message>"

def execute(**kwargs):
    # extract bot command + arguments:
    bot_command_mo = re.match(r"([\w]+)[\s]+(.*)", kwargs['arguments'])

    if bot_command_mo:
        nick = bot_command_mo.group(1)
        message = bot_command_mo.group(2)

        def action(match_object):
        irc.send_to_channel(kwargs['channel'], "%s: %s wanted me to tell you: %s" % (nick, kwargs['caller_nick'], message))

        # ':blaine!blaine@Clk-E28261F1 PRIVMSG #test :#tell'
        action = Action(
            run_once=True,
            regex=r"^:%s![^\s]+ PRIVMSG %s :.*" % (nick, kwargs['channel']),
            action=action
        )
        irc.send_to_channel(kwargs['channel'], "Ok, I will tell %s the next time I see them." % nick)
        MessageInterpreter.action_insertion_queue.append(action)
    else:
        irc.send_to_channel(kwargs['channel'], USAGE)
