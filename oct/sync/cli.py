import click


@click.group()
def sync():
    click.echo("placeholder for `sync` functionality: updating source code revision on the host")
