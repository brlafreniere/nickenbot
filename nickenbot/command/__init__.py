import os
import fnmatch
import string
import importlib
import traceback
from .. import irc

def get_all():
    files = os.listdir('./nickenbot/command')
    files.remove('__init__.py')
    commands = [os.path.splitext(f)[0] for f in files if fnmatch.fnmatch(f, '*.py')]
    commands = [string.replace(c, '_', '-') for c in commands]
    return commands

def execute(**kwargs):
    print(kwargs['command'])
    command = string.replace(kwargs['command'], '-', '_')
    print(command)
    module_string = string.join([__name__, command], '.')

    module = None
    try:
        module = importlib.import_module(module_string)
    except ImportError as e:
        traceback.print_exc()
        irc.send_to_channel(kwargs['channel'], "No such command.")

    if not module == None: 
        module.execute(**kwargs)
