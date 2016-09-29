# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import ClickException, argument, command, echo, pass_context

_short_help = 'Update a setting in the serialized configuration.'


@command(
    name='set',
    short_help=_short_help,
    help=_short_help + '''

Existing configuration options that are used by default
for every interaction with Ansible can be edited with
this command.

\b
Examples:
  Update the option 'become_method' option to 'pfexec'
  $ oct config set 'become_method' 'pfexec'
'''
)
@argument(
    'option'
)
@argument(
    'value'
)
@pass_context
def set_command(context, option, value):
    """
    Update a setting in the configuration file.

    :param context: Click context
    :param option: name of the option to update
    :param value: value to update to
    """
    configuration = context.obj
    if option not in configuration:
        raise ClickException(message='Option ' + option + ' not found in configuration.')

    configuration[option] = value
    configuration.write_configuration()

    echo('Option %r updated to be %r.' % (str(option), str(value)))  # use str.format
