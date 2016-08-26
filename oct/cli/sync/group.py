import click


@click.group(
    short_help='Synchronize the repositories on the host with their remotes.'
)
def sync():
    click.echo("placeholder for `sync` functionality: updating source code revision on the host")
