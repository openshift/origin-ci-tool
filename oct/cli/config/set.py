# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import argument, command, echo

from ...config import CONFIG
from ...config.load import update_config

_short_help = 'Update or append to the serialized configuration.'


@command(
    short_help=_short_help,
    help=_short_help + '''

Existing configuration options can be edited, or new
configuration options can be added to the set of all
configurations that are used by default for every
interaction with Ansible.

\b
Examples:
  Update the option 'become_method' option to 'pfexec'
  $ oct config set 'become_method' 'pfexec'
\b
  Add a new option 'ssh_extra_args' with value '-l'
  $ oct config set 'ssh_extra_args' '-l'
'''
)
@argument(
    'option'
)
@argument(
    'value'
)
def set(option, value):
    """
    Update or append to the configuration file.

    :param option: name of the option to update or append
    :param value: value to update to or append
    """
    verb = 'added to'
    if option in CONFIG['config']:
        verb = 'updated in'

    CONFIG['config'][option] = value
    update_config()

    echo('Option %r %s the configuration to be %r.' % (str(option), verb, str(value)))
