import click
from cli.config.remove import remove
from cli.config.set import set
from cli.config.show import show


@click.group(
    short_help='View, update and append to the serialized configuration.',
    help='''
Common configuration options for Ansible are stored in serialized
form per-user on the file system of the controlling host. These
files should not be edited by hand; rather, they should be viewed
and updated using these command-line endpoints.
'''
)
def config():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


config.add_command(remove)
config.add_command(set)
config.add_command(show)
