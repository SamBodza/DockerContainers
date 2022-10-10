import yaml
import os


def get_yaml(logger):
    """Parses Yaml file into Dict
    can be accessed like valuesYaml['global']['dbConnectionString']"""
    path = os.path.join(os.path.dirname(__file__), "../config/config.yml")
    try:
        with open(path, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        logger.critical(f'failed to parse yaml: {e}')
        raise Exception

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), "../config/config.yml")
    try:
        with open(path, 'r') as f:
            file = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print(e)

    for fmt in file['Extensions']:
        try:
            print(str(fmt).encode().decode('unicode_escape'))
        except Exception as e:
            pass