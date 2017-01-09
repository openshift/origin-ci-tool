# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, option, pass_context

from ..util.common_options import ansible_output_options

_short_help = 'Download Origin test artifacts from the remote host.'


@command(
    short_help=_short_help,
    name='origin-artifacts',
    help=_short_help + '''

To preserve information about tests run on the remote system and
to allow for better debugging, it is possible to download the
test artifacts generated on the remote host.

\b
Usage:
  Download Origin test artifacts
  $ oct download origin-artifacts --dest='./artifacts'
''',
)
@option(
    '--dest', '-d',
    metavar='DIR',
    required=True,
    help='Destination directory for artifacts.',
)
@ansible_output_options
@pass_context
def origin_artifacts(context, dest):
    """
    Download Origin test artifacts from the remote host.

    :param context: Click context
    :param dest: local dir where artifacts will be downloaded to
    """
    ansible_client = context.obj
    ansible_client.run_playbook(
        playbook_relative_path='download/main',
        playbook_variables={
            'origin_ci_artifacts_destination_dir': dest,
            'origin_ci_download_targets': ['/tmp/openshift'],
        },
    )
