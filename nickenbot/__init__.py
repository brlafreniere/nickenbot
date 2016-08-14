import connection

def run():
    conn = connection.ServerConnection()

    while True:
        self.message_interpreter.process_messages(self.receive_messages())

        if not self.registered:
            self.register_nick_and_username()
            self.registered = True
