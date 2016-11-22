# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, pass_context

from ..util.common_options import ansible_output_options

_short_help = 'Bootstrap the local host to support this CLI.'


@command(
    short_help=_short_help,
    help=_short_help + '''

In order for a machine to run all of the tasks that this CLI knows how
to run, a set of requisite dependencies need to be installed first. This
command will install them on the local host.

\b
Examples:
  Bootstrap the local host
  $ oct bootstrap self
'''
)
@ansible_output_options
@pass_context
def self(context):
    """
    Bootstrap the local host to support this CLI.

    :param context: Click context
    """
    context.obj.run_playbook(
        playbook_relative_path='bootstrap/self'
    )
