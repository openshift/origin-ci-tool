import click
from cli.util.common_options import ansible_output_options
from util.playbook import playbook_path
from util.playbook_runner import PlaybookRunner


@click.command(
    short_help='Bootstrap a machine to be an Ansible controller node.',
    help='''
Bootstraps a machine to be an Ansible controller node.

In order for a machine to run Ansible playbooks, a set of requisite
dependencies need to be installed first. This command will install them
as well as a copy of this tool so that the node can be used to modify
itself.

\b
Examples:
  Bootstrap a machine
  $ oct boostrap node
'''
)
@ansible_output_options
def node():
    """
    Bootstrap a machine to be an Ansible controller node.
    """
    PlaybookRunner().run(
        playbook_source=playbook_path('bootstrap/node')
    )
