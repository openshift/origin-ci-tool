import click
from __future__ import absolute_import, division, print_function


@click.group(
    short_help='Install and configure systems from binaries and artifacts.'
)
def install():
    click.echo("placeholder for `install` functionality: installing binaries/RPMs/images")
