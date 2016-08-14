import re

import config
import command

from connection import ServerConnection

class ActionTrigger:
    action_triggers = []

    def __init__(self, run_once=False, **kwargs):
        self.regex = kwargs['regex']
        self.action = kwargs['action']
        self.run_once = run_once

        ActionTrigger.action_triggers.append(self)

    def check(self, message):
        match = re.match(self.regex, message)
        if match:
            self.execute_action(match)
            if self.run_once:
                action_triggers.remove(self)

    def execute_action(self, match_object):
        self.action(match_object)
        if self.run_once:
            action_triggers.remove(self)

class MessageInterpreter:
    def __init__(self, servconn):

        # Bot command action
        # :blaine!blaine@Clk-E28261F1 PRIVMSG #test :.tell
        ActionTrigger(
            regex=r":(\w*)!.*.*PRIVMSG ([^\s]+) :%s([\w]+)[\s]*(.*)" % re.escape(config.get('command_prefix')),
            action=lambda match: command.execute(connection, caller_nick=match.group(1), channel=match.group(2), command=match.group(3), arguments=match.group(4))
        )

        # Pinging
        ActionTrigger(
            regex=r"^PING .*",
            action=lambda match: servconn.pong(match.group(0))
        )

        # Connection accepted (AKA RPL_WELCOME, status 001)
        ActionTrigger(
            regex=r".* 001 %s" % config.get('nick'),
            action=lambda match: servconn.join_config_channels()
        )

        # Nickname registered already
        ActionTrigger(
            regex=r"NOTICE.*nickname.*registered",
            action=lambda match: servconn.identify_with_nickserv()
        )
    
    def process_messages(self, messages):
        for message in messages:
            for action_trigger in ActionTrigger.action_triggers:
                if action_trigger.check(message):
                    break
