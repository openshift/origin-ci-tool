import click
from cli.provision.vagrant import vagrant

_short_help = 'Provision a virtual machine for continuous integration tasks.'


@click.group(
    short_help=_short_help,
    help=_short_help + '''

'''
)
def provision():
    click.echo("placeholder for `provision` functionality: creating a naked host")


provision.add_command(vagrant)
