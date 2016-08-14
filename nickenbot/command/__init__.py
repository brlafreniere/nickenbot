import os
import string
import importlib
import traceback
from .. import irc

def execute(**kwargs):
    print (kwargs['command'] + " command received.")

    module_string = string.join([__name__, kwargs['command']], '.')
    print("Importing module: " + module_string)

    module = None
    try:
        module = importlib.import_module(module_string)
    except ImportError as e:
        traceback.print_exc()
        irc.send_to_channel(kwargs['channel'], "No such command.")

    module.execute(**kwargs)
