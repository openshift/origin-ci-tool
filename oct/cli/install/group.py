import click


@click.group(
    short_help='Install and configure systems from binaries and artifacts.'
)
def install():
    click.echo("placeholder for `install` functionality: installing binaries/RPMs/images")
