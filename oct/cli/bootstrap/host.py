from __future__ import absolute_import, division, print_function

from click import command

from ..util.common_options import ansible_output_options
from ...util.playbook import playbook_path
from ...util.playbook_runner import PlaybookRunner

_short_help = 'Bootstrap a machine to be an Ansible target host.'


@command(
    short_help=_short_help,
    help=_short_help + '''

In order for Ansible to interact with a target host, a set of requisite
dependencies need to be installed first. This command will install them
using the `raw` module, so these actions will not be idempotent.

\b
Examples:
  Bootstrap a machine
  $ oct bootstrap host
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
