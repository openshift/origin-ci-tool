import click


@click.group()
def prepare():
    click.echo("placeholder for `prepare` functionality: installing dependencies onto a naked host")
