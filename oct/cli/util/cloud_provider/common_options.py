# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Choice, option


class Provider(object):
    """
    An enumeration of supported clouds for provisioning
    of VMs.
    """
    aws = 'aws'


def provider_option(func):
    """
    Add option to decorated command func for specifying cloud provider (e.g. AWS, GCP, etc.)

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--provider',
        '-p',
        type=Choice([Provider.aws, ]),
        default=Provider.aws,
        show_default=True,
        metavar='NAME',
        help='Cloud provider.',
    )(func)
