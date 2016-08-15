import os
import string
import importlib
import traceback
from .. import irc

def execute(**kwargs):
    module_string = string.join([__name__, kwargs['command']], '.')

    module = None
    try:
        module = importlib.import_module(module_string)
    except ImportError as e:
        traceback.print_exc()
        irc.send_to_channel(kwargs['channel'], "No such command.")

    if not module == None: 
        module.execute(**kwargs)
