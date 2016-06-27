import yaml

def get(key):
    config_file = open('config.yaml', 'r')
    config = yaml.load(config_file.read())
    return config[key]
