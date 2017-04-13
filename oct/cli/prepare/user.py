# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, pass_context

from ..util.common_options import ansible_output_options

_SHORT_HELP = 'Configure the CI user on remote hosts.'


@command(
    name='user',
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

The `origin' user is created on the remote machine and
will be used by default for all CI actions on the machine.

\b
Examples:
  Prepare the CI user
  $ oct prepare user
''',
)
@ansible_output_options
@pass_context
def user(context):
    """
    Configures the CI user on the remote host.

    :param context: Click context
    """
    context.obj.run_playbook(playbook_relative_path='prepare/user')
