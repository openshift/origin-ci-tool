import click
import config
from config.load import update_config


@click.command(
    short_help='Update or append to the serialized configuration.',
    help='''
Updates or appends to the serialized configuration.

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
@click.argument(
    'option'
)
@click.argument(
    'value'
)
def set(option, value):
    """
    Update or append to the configuration file.

    :param option: name of the option to update or append
    :param value: value to update to or append
    """
    verb = 'added to'
    if option in config._config:
        verb = 'updated in'

    config._config[option] = value
    update_config()

    click.echo('Option %r %s the configuration to be %r.' % (str(option), verb, str(value)))
