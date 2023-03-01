import json
import os


CONF_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/config/"


with open(CONF_DIR + "ide_config.json") as conf_file:
    config_data = json.load(conf_file)
