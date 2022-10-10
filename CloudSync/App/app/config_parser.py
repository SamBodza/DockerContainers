import os
from configparser import ConfigParser


def get_config():
    """Returns config object for SQL connection String"""
    config_object = ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), "../config/config.ini")
        config_object.read(path)
        test = config_object['SQL']
    except Exception as e:
        print(e)

    return config_object
