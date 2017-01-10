# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .local import local
from .remote import remote

_SHORT_HELP = 'Update the state of repositories on the virtual machine.'


@group(
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

When developing one of the repositories in the OpenShift
ecosystem, it is necessary to update the source code on
the remote machines managed by this tool in order to build,
install, and test the changes. These commands allow for
synchronization of the remote repositories with local sources
or remote servers.
''',
)
def sync():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


sync.add_command(local)
sync.add_command(remote)
