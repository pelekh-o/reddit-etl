from configparser import RawConfigParser, NoSectionError
from os.path import join, dirname


def get_config_section(section):
    config = RawConfigParser()
    config_file = 'pipeline.conf'
    config.read(join(dirname(__file__), config_file))
    try:
        configs_dict = dict(config.items(section))
    except NoSectionError:
        print(f'The {section} section cannot be found in the {config_file} config file.')
    return configs_dict