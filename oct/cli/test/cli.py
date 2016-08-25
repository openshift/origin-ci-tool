import click


@click.group()
def test():
    click.echo("placeholder for `test` functionality: shelling out to Makefiles for actions after builds/installs")
