from __future__ import absolute_import, division, print_function
from collections import namedtuple

import config


def default_options(options):
    """
    Default unset values in options using values loaded from
    on-disk configuration.

    :param options: partially-filled Ansible options
    :return: defaulted Ansible options
    """
    for option in options:
        if options[option] is None and option in config._config:
            options[option] = config._config[option]

    return namedtuple('Options', options.keys())(**options)


def default_inventory(host_list):
    """
    Default the inventory or host list using values loaded from
    on-disk configuration.

    :param host_list: a comma-delimited list of hosts or path to an inventory
    :return: defaulted inventory or list of hosts
    """
    if not host_list:
        return config._config['host_list']

    return host_list
