from configparser import RawConfigParser, NoSectionError
from os.path import join, dirname

PIPELINE_CONF = 'pipeline.conf'


def get_config_section(section, config_file=None):
    config = RawConfigParser()
    if not config_file:
        config_file = PIPELINE_CONF
    config.read(join(dirname(__file__), config_file))
    try:
        configs_dict = dict(config.items(section))
    except NoSectionError:
        print(f'The {section} section cannot be found in the {config_file} config file.')
    return configs_dict
