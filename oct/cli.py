import click

from build.cli import build
from install.cli import install
from prepare.cli import prepare
from provision.cli import provision
from sync.cli import sync
from test.cli import test


@click.group()
def oct():
    click.echo("placeholder for root helptext functionality")


oct.add_command(build)
oct.add_command(install)
oct.add_command(prepare)
oct.add_command(provision)
oct.add_command(sync)
oct.add_command(test)
