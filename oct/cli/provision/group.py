import click
from cli.provision.vagrant import vagrant


@click.group(
    short_help='Provision a virtual machine for continuous integration tasks.'
)
def provision():
    click.echo("placeholder for `provision` functionality: creating a naked host")


provision.add_command(vagrant)
