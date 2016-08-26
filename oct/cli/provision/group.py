import click


@click.group(
    short_help='Provision a host to use for continuous integration tasks.'
)
def provision():
    click.echo("placeholder for `provision` functionality: creating a naked host")
