# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, pass_context

from .util.common_options import ansible_output_options

_short_help = 'Remove provisioned VMs and local artifacts.'


@command(
    short_help=_short_help,
    help=_short_help + '''

Remove the virtual machines that were provisoned and
delete local artifacts that were used by this tool to
track those machines, to clean up an environment created
with this tool.

\b
Examples:
  Clean up the development environment
  $ oct deprovision
''',
)
@ansible_output_options
@pass_context
def deprovision(context):
    """
    Remove provisioned VMs and local artifacts.

    :param context: Click context
    """
    context.obj.run_playbook(
        playbook_relative_path='deprovision/main',
        playbook_variables={'origin_ci_inventory_dir': context.obj.ansible_client_configuration.host_list, },
    )
