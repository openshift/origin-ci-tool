import click


@click.group(
    short_help='Build binaries and other artifacts from source code.'
)
def build():
    click.echo("placeholder for `build` functionality: create binaries/images/RPMs from source")
