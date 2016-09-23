import copy
import os
from __future__ import absolute_import, division, print_function

import click
import config
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
    config._vagrant_home = config._config_home + 'vagrant'


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
            click.UsageError('Could not load origin-ci-tool configuration at: ' + config._config_path + ': ' + exception.message)


def update_config():
    """
    Update the Ansible configuration on disk.
    """
    with open(config._config_path, 'w') as config_file:
        try:
            yaml.dump(config._config, config_file, default_flow_style=False)
        except yaml.YAMLError as exception:
            click.UsageError('Could not save origin-ci-tool configuration at: ' + config._config_path + ': ' + exception.message)


def safe_update_config():
    """
    Update the Ansible configuration on file, without
    touching any of the options that can be set by run-
    time flags and are expected not to persist past one
    CLI interaction.

    Use this to update configuration inside of CLI end-
    points so that options like `-vvvvvv` don't stick
    around.
    """
    with open(config._config_path, 'r+') as config_file:
        current_config = yaml.load(config_file)
        runtime_config_copy = copy.deepcopy(config._config)
        runtime_config_copy['verbosity'] = current_config['verbosity']
        runtime_config_copy['check'] = current_config['check']
        try:
            config_file.seek(0)
            config_file.truncate(0)
            yaml.dump(runtime_config_copy, config_file, default_flow_style=False)
        except yaml.YAMLError as exception:
            click.UsageError('Could not save origin-ci-tool configuration at: ' + config._config_path + ': ' + exception.message)


def add_host_to_inventory(host):
    """
    Update the Ansible inventory to add a hostname.

    :param host: name of host to add
    """
    with open(config._inventory_path, 'a') as inventory_file:
        inventory_file.write(host + '\n')


def remove_host_from_inventory(host):
    """
    Update the Ansible inventory to remove a hostname.

    :param host: name of host to remove
    """
    with open(config._inventory_path, 'r+') as inventory_file:
        entries = inventory_file.readlines()
        inventory_file.seek(0)
        inventory_file.truncate(0)
        for entry in entries:
            if entry.rstrip('\n') != host:
                inventory_file.write(entry)
        inventory_file.truncate()


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
