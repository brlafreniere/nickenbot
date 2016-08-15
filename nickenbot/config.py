import yaml
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.realpath(os.path.join(current_dir, ".."))

class ConfigManager:
    network = None
    config = None

    @classmethod
    def load(clss):
        if clss.network:
            config_filepath = os.path.join(project_dir, 'config/%s.config.yaml' % clss.network)
        else:
            config_filepath = os.path.join(project_dir, 'config/config.yaml')

        config_file = open(config_filepath, 'r')
        config_yaml = config_file.read()
        clss.config = yaml.load(config_yaml)

    @classmethod
    def get(clss, key):
        if not clss.config:
            clss.load()
            if not clss.config:
                print("Configuration not found. Exiting.")
                sys.exit(1)
        return clss.config[key]
