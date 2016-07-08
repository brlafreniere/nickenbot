import yaml
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.realpath(os.path.join(current_dir, ".."))
config_filepath = os.path.join(project_dir, 'config/config.yaml')
config_file = open(config_filepath, 'r')
config_yaml = config_file.read()
config = yaml.load(config_yaml)

def get(key):
    return config[key]

def display():
    print(config_yaml + "\n")
