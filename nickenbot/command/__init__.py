import os
import string
import importlib

def execute(connection, **kwargs):
    try:
        module = importlib.import_module(string.join([__name__, kwargs['command']], '.'))
        module.execute(kwargs)
    except ImportError:
        connection.send_to_channel(kwargs['channel'], "No such command.")
