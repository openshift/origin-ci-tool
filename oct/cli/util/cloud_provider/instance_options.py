# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import option


def instance_name_option(func):
    """
    Add option to decorated command func for specifying human-readable name for a VM instance

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--name',
        '-n',
        metavar='NAME',
        required=True,
        help='VM instance name.',
    )(func)
