# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, option, pass_context

from ..util.common_options import ansible_output_options

_SHORT_HELP = 'Bootstrap the local host to support this CLI.'


@command(
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

In order for a machine to run all of the tasks that this CLI knows how
to run, a set of requisite dependencies need to be installed first. This
command will install them on the local host.

\b
Examples:
  Bootstrap the local host
  $ oct bootstrap self
''',
)
@option(
    '--for-images',
    '-i',
    'for_images',
    is_flag=True,
    help='Install dependencies for VM image building.',
)
@ansible_output_options
@pass_context
def self(context, for_images):
    """
    Bootstrap the local host to support this CLI.

    :param context: Click context
    :param for_images: whether or not to bootstrap image build dependencies
    """
    context.obj.run_playbook(
        playbook_relative_path='bootstrap/self',
        playbook_variables={'origin_ci_bootstrap_image_dependencies': for_images, },
    )
