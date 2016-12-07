# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, option, pass_context

from .common_options import package_options
from ..util.common_options import ansible_output_options

_short_help = 'Package a running AWS EC2 virtual machine.'


@command(
    short_help=_short_help,
    help=_short_help + '''

This command allows for a virtual machine in EC2 to be packaged
as an update for its current stage or as an instance of the next
stage in the pipeline.

\b
Examples:
  Package a VM as a stage upgrade
  $ oct package ami --upgrade
'''
)
@option(
    '--name-suffix', '-n',
    'suffix',
    required=True,
    help='Suffix for AMI name for uniqueness.'
)
@ansible_output_options
@package_options
@pass_context
def ami(context, update_current_stage, suffix):
    """
    Package a running AWS EC2 virtual machine.

    :param context: Click context
    :param update_current_stage: whether or not to update current stage
    """
    configuration = context.obj
    configuration.run_playbook(
        playbook_relative_path='package/ami',
        playbook_variables={
            'origin_ci_aws_stage_strategy': 'update' if update_current_stage else 'upgrade',
            'origin_ci_inventory_dir': configuration.ansible_client_configuration.host_list,
            'origin_ci_aws_ami_name_suffix': suffix
        }
    )
