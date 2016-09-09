import click
from ansible.cli import CLI


@click.command(
    short_help='Print version information for this tool.',
    help='''
Print version information for this tool.

As this tool bundles a number of other tools to achieve
its goals, the version of all of those tools is important
to fully define the system.
'''
)
def version():
    """
    Print version information.
    """
    click.echo('origin-ci-tool version:')
    click.echo('\toct 0.1.0\n')
    click.echo('ansible version:')
    click.echo(''.join(['\t' + line + '\n' for line in CLI.version('ansible').splitlines()]))
    click.echo('openshift-ansible version:')
    click.echo('\tTODO')
    click.echo('openshift-ansible-contrib version:')
    click.echo('\tTODO')
