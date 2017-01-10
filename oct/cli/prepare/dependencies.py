# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, pass_context

from ..util.common_options import ansible_output_options

_SHORT_HELP = 'Install system dependencies on remote hosts.'


@command(
    name='dependencies',
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

If a preset is chosen, default values for the other options are used
and user-provided options are ignored.

\b
Examples:
  Install system dependencies
  $ oct prepare dependencies
''',
)
@ansible_output_options
@pass_context
def dependencies(context):
    """
    Installs the system dependencies on the remote host.

    :param context: Click context
    """
    context.obj.run_playbook(playbook_relative_path='prepare/dependencies', )
