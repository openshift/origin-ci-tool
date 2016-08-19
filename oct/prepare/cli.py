import click
from prepare.docker import docker
from prepare.golang import golang


@click.group()
def prepare():
    click.echo("placeholder for `prepare` functionality: installing dependencies onto a naked host")


prepare.add_command(golang)
prepare.add_command(docker)
