import click


@click.group(
    short_help='Run tests and other tasks for a synchronized repository.'
)
def test():
    click.echo("placeholder for `test` functionality: shelling out to Makefiles for actions after builds/installs")
