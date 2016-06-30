import os
import string
import importlib

def execute(channel, command, arguments, connection):
    try:
        module = importlib.import_module(string.join([__name__, command], '.'))
        module.execute(arguments, channel, connection)
    except ImportError:
        connection.send_to_channel(channel, "No such command.")
