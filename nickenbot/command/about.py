from .. import irc

about_text = "A simple bot written in Python. Source: https://github.com/brlafreniere/nickenbot"

def execute(**kwargs):
    irc.send_to_channel(kwargs['channel'], about_text)
