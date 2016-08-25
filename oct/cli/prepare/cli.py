import click
from .docker import docker
from .golang import golang


@click.group()
def prepare():
    click.echo("placeholder for `prepare` functionality: installing dependencies onto a naked host")


prepare.add_command(golang)
prepare.add_command(docker)
