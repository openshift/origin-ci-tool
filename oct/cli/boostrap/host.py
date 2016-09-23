import click
from cli.util.common_options import ansible_output_options
from util.playbook import playbook_path
from util.playbook_runner import PlaybookRunner
from __future__ import absolute_import, division, print_function

_short_help = 'Bootstrap a machine to be an Ansible target host.'


@click.command(
    short_help=_short_help,
    help=_short_help + '''

In order for Ansible to interact with a target host, a set of requisite
dependencies need to be installed first. This command will install them
using the `raw` module, so these actions will not be idempotent.

\b
Examples:
  Bootstrap a machine
  $ oct boostrap host
'''
)
@ansible_output_options
def host():
    """
    Bootstrap a machine to be an Ansible target host.
    """
    PlaybookRunner().run(
        playbook_source=playbook_path('bootstrap/host')
    )
