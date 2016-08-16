import re
import string
import os
import fnmatch

from .. import irc, command

def execute(**kwargs):
    irc.send_to_channel(kwargs['channel'], "all available commands: %s." % string.join(command.get_all(), ', '))
