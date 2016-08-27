import sys

import click
import config
import os
import yaml
from config.default import default_config, default_inventory


def initialize_paths():
    """
    Initialize configuration paths. Configuration will be placed
    in the user-based configuration path as per the XDG basedir
    specification:
    https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    """
    config._config_home = os.getenv('XDG_CONFIG_HOME', os.environ['HOME'] + '/.config/origin-ci-tool/')
    config._config_path = config._config_home + 'config.yml'
    config._inventory_path = config._config_home + 'inventory'


def load_config():
    """
    Load the origin-ci-tool configuration file from disk.
    If the configuration directory does not exist, it will
    be created and filled with default values.
    """
    if os.path.exists(config._config_home):
        if not os.path.isdir(config._config_home):
            # something is in our config dir, but it is not our
            # config dir -- we want to delete whatever is there
            # and place a new directory there to use
            os.remove(config._config_home)
            write_defaults()
            return
    else:
        # our config dir does not exist yet, so we should create it
        write_defaults()
        return

    with open(config._config_path, 'r') as config_file:
        try:
            config._config = yaml.load(config_file)
        except yaml.YAMLError as exception:
            click.echo('Could not load origin-ci-tool configuration at: ' + config._config_path + ': ' + exception.message)
            sys.exit(1)


def update_config():
    """
    Update the system configuration in our local cache and
    also on disk.
    """
    with open(config._config_path, 'w') as config_file:
        try:
            yaml.dump(config._config, config_file)
        except yaml.YAMLError as exception:
            click.echo('Could not save origin-ci-tool configuration at: ' + config._config_path + ': ' + exception.message)
            sys.exit(1)


def write_defaults():
    """
    Initialize the configuration directory and write defaults
    to all the constituent files.
    """
    os.mkdir(config._config_home)
    config._config = default_config()
    update_config()

    with open(config._inventory_path, 'w') as inventory_file:
        inventory_file.write(default_inventory())
