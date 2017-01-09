# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, pass_context

from ..util.common_options import ansible_output_options

_short_help = 'Initialize source code repositories.'


@command(
    short_help=_short_help,
    help=_short_help + '''

In order to sync or build from source code on the virtual
machine, or install from the artifacts created from the build,
the source code repositories must first be present on the
virtual machine. This command will ensure that an up-to-date
copy of the repositories checked out to origin:master/HEAD
exists for every repository.

\b
Examples:
  Initialize all source code repositories
  $ oct prepare repositories
''',
)
@ansible_output_options
@pass_context
def repositories(context):
    """
    Initialize source code repositories on the target hosts.

    :param context: Click context
    """
    context.obj.run_playbook(playbook_relative_path='prepare/repositories', )
