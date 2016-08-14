import connection
servconn = connection.ServerConnection()

import irc

from parsing import MessageInterpreter

def run():

    while True:
        message_interpreter = MessageInterpreter(servconn)
        message_interpreter.process_messages(servconn.receive_messages())

        if not servconn.registered:
            irc.register_nick_and_username()
            servconn.registered = True
