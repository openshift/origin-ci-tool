import click
import config
from config.load import update_config
from __future__ import absolute_import, division, print_function

_short_help = 'Remove an option from the serialized configuration.'


@click.command(
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
@click.argument(
    'option'
)
def remove(option):
    """
    Remove an option from the configuration file.

    :param option: name of the option to remove
    """
    del config._config[option]
    update_config()

    click.echo('Option %r removed from the configuration.' % str(option))
