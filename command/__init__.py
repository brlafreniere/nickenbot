import os
import string
import importlib

def execute(channel, command, arguments, connection):
    module = importlib.import_module(string.join([__name__, command], '.'))
    module.execute(arguments, channel, connection)
