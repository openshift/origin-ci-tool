import click

from cli.build.cli import build
from cli.install.cli import install
from cli.prepare.cli import prepare
from cli.provision.cli import provision
from cli.sync.cli import sync
from cli.test.cli import test


@click.group()
def oct():
    click.echo("placeholder for root helptext functionality")


oct.add_command(build)
oct.add_command(install)
oct.add_command(prepare)
oct.add_command(provision)
oct.add_command(sync)
oct.add_command(test)
