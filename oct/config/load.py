# coding=utf-8
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from click import UsageError
from os import environ, getenv, mkdir, path, remove
from yaml import YAMLError, dump, load

from .default import default_config, default_inventory

# these module-level "private" dictionary keys will hold our
# in-memory cache of information regarding configuration
CONFIG = {
    'config': {},
    'config_home': '',
    'vagrant_home': '',
    'inventory_path': ''
}


def initialize_paths():
    """
    Initialize configuration paths. Configuration will be placed
    in the user-based configuration path as per the XDG basedir
    specification:
    https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    """
    CONFIG['config_home'] = getenv('XDG_CONFIG_HOME', environ['HOME'] + '/.config/origin-ci-tool/')
    CONFIG['config_path'] = CONFIG['config_home'] + 'config.yml'
    CONFIG['inventory_path'] = CONFIG['config_home'] + 'inventory'
    CONFIG['vagrant_home'] = CONFIG['config_home'] + 'vagrant'


def load_config():
    """
    Load the origin-ci-tool configuration file from disk.
    If the configuration directory does not exist, it will
    be created and filled with default values.
    """
    if path.exists(CONFIG['config_home']):
        if not path.isdir(CONFIG['config_home']):
            # something is in our config dir, but it is not our
            # config dir -- we want to delete whatever is there
            # and place a new directory there to use
            remove(CONFIG['config_home'])
            write_defaults()
            return
    else:
        # our config dir does not exist yet, so we should create it
        write_defaults()
        return

    with open(CONFIG['config_path']) as config_file:
        try:
            CONFIG['config'] = load(config_file)
        except YAMLError as exception:
            raise UsageError('Could not load origin-ci-tool configuration at: ' + CONFIG['config_path'] + ': ' +
                             exception.message)


def update_config():
    """
    Update the Ansible configuration on disk.
    """
    with open(CONFIG['config_path'], 'w') as config_file:
        try:
            dump(CONFIG['config'], config_file, default_flow_style=False)
        except YAMLError as exception:
            raise UsageError('Could not save origin-ci-tool configuration at: ' + CONFIG['config_path'] + ': ' +
                             exception.message)


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
    with open(CONFIG['config_path'], 'r+') as config_file:
        current_config = load(config_file)
        runtime_config_copy = deepcopy(CONFIG['config'])
        runtime_config_copy['verbosity'] = current_config['verbosity']
        runtime_config_copy['check'] = current_config['check']
        try:
            config_file.seek(0)
            config_file.truncate(0)
            dump(runtime_config_copy, config_file, default_flow_style=False)
        except YAMLError as exception:
            raise UsageError('Could not save origin-ci-tool configuration at: ' + CONFIG['config_path'] + ': ' +
                             exception.message)


def add_host_to_inventory(host):
    """
    Update the Ansible inventory to add a hostname.

    :param host: name of host to add
    """
    with open(CONFIG['inventory_path'], 'a') as inventory_file:
        inventory_file.write(host + '\n')


def remove_host_from_inventory(host):
    """
    Update the Ansible inventory to remove a hostname.

    :param host: name of host to remove
    """
    with open(CONFIG['inventory_path'], 'r+') as inventory_file:
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
    mkdir(CONFIG['config_home'])
    CONFIG['config'] = default_config(CONFIG['inventory_path'])
    update_config()

    with open(CONFIG['inventory_path'], 'w') as inventory_file:
        inventory_file.write(default_inventory())


initialize_paths()
load_config()
