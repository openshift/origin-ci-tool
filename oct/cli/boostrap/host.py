import click
from cli.util.common_options import ansible_verbosity_option, ansible_dry_run_option, ansible_debug_mode_option
from util.playbook import playbook_path
from util.playbook_runner import PlaybookRunner


@click.command(
    short_help='Bootstrap a machine to be an Ansible target host.',
    help='''
Bootstraps a machine to be an Ansible target host.

In order for Ansible to interact with a target host, a set of requisite
dependencies need to be installed first. This command will install them
using the `raw` module, so these actions will not be idempotent.

\b
Examples:
  Bootstrap a machine
  $ oct boostrap host
'''
)
@ansible_verbosity_option
@ansible_dry_run_option
@ansible_debug_mode_option
def host():
    """
    Bootstrap a machine to be an Ansible target host.
    """
    PlaybookRunner().run(
        playbook_source=playbook_path('bootstrap/host')
    )
