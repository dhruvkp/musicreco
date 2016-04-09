import yaml

configfile = "config.yaml"
settings = {}

with open(configfile, 'r') as f:
    #s = f.read()
    settings = yaml.load(f)
