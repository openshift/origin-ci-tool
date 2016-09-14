import click
from cli.prepare.all import all
from cli.prepare.docker import docker
from cli.prepare.golang import golang
from cli.prepare.repositories import repositories


@click.group(
    short_help='Prepare a host by installing and configuring dependencies.',
    help='''
Once new hosts have been provisioned or existing hosts have been
registered, all hosts that will be running Origin continuous
integration tasks need to be prepared. The preparation process
includes installation of the full suite of dependencies for the
OpenShift installation and all of the testing tasks.

A full preparation will install all necessary dependencies, but
dependencies that vary by OpenShift version can be changed after
the fact.
'''
)
def prepare():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


prepare.add_command(all)
prepare.add_command(docker)
prepare.add_command(golang)
prepare.add_command(repositories)
