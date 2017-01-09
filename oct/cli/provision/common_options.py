# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import option


def discrete_ssh_config_option(func):
    """
    Add the discrete SSH config option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--discrete-ssh-config', '-g',
        'discrete_ssh_config',
        is_flag=True,
        help='Write SSH config to a discrete file.',
    )(func)
