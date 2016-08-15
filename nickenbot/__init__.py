import connection
servconn = connection.ServerConnection()

import irc

from parsing import MessageInterpreter, Action

def run():
    MessageInterpreter.register_default_actions()

    while True:
        Action.actions = Action.actions + MessageInterpreter.action_insertion_queue
        MessageInterpreter.action_insertion_queue = []

        messages = servconn.receive_messages()
        MessageInterpreter.process_messages(messages)

        if not servconn.registered:
            irc.register_nick_and_username()
            servconn.registered = True
