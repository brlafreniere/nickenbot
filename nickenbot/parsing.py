import re

from config import ConfigManager
import command
import irc

class Action:
    actions = []

    def __init__(self, run_once=False, **kwargs):
        self.regex = kwargs['regex']
        self.action = kwargs['action']
        self.run_once = run_once

    def execute(self, action_mo):
        self.action(action_mo)

    def check_match_and_execute(self, message):
        action_mo = re.match(self.regex, message)
        if action_mo:
            self.action(action_mo)
            if self.run_once:
                Action.actions.remove(self)

class MessageInterpreter:
    action_insertion_queue = []

    @staticmethod
    def register_default_actions():
        def bot_command_action(bot_command_mo):
            command.execute(
                caller_nick=bot_command_mo.group(1),
                channel=bot_command_mo.group(2),
                command=bot_command_mo.group(3),
                arguments=bot_command_mo.group(4)
            )

        # Bot command action
        # :blaine!blaine@Clk-E28261F1 PRIVMSG #test :.tell
        actions = [Action(
            regex=r"^:([^\s]+)![^\s]+ PRIVMSG ([^\s]+) :%s([\w-]+)[\s]*(.*)" % re.escape(ConfigManager.get('command_prefix')),
            action=bot_command_action
        ),

        # Pinging
        Action(
            regex=r"^PING .*",
            action=lambda match_object: irc.pong(match_object.group(0))
        ),

        # Connection accepted (AKA RPL_WELCOME, status 001)
        Action(
            regex=r".* 001 %s" % ConfigManager.get('nick'),
            action=lambda match_object: irc.join_config_channels()
        ),

        # Nickname registered already
        # ':NickServ!NickServ@snoonet/services/NickServ NOTICE nickenbot :This nickname is registered and protected.  If it is your'

        Action(
            regex=r"^:NickServ!NickServ@[^\s]+ NOTICE %s :.*registered.*" % ConfigManager.get('nick'),
            action=lambda match_object: irc.identify_with_nickserv()
        )]
        Action.actions = actions
    
    @staticmethod
    def process_messages(messages):
        for message in messages:
            for action in Action.actions:
                if action.check_match_and_execute(message):
                    break
