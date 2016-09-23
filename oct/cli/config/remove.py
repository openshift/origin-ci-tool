# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import UsageError, argument, command, echo

from ...config import CONFIG
from ...config.load import update_config

_short_help = 'Remove an option from the serialized configuration.'


@command(
    short_help=_short_help,
    help=_short_help + '''

Existing configuration options can be removed from
the set of all configurations that are used by default
for every interaction with Ansible.

\b
Examples:
  Remove the option 'become_method' option
  $ oct config remove 'become_method'
'''
)
@argument(
    'option'
)
def remove(option):
    """
    Remove an option from the configuration file.

    :param option: name of the option to remove
    """
    if option not in CONFIG['config']:
        raise UsageError('Option %r not found in the configuration.' % str(option))

    del CONFIG['config'][option]
    update_config()

    echo('Option %r removed from the configuration.' % str(option))
