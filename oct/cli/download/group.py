# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .origin_artifacts import origin_artifacts


@group(
    short_help='Download files from remote hosts.',
    help='''
Once actions have been executed on remote hosts, this command
allows for downloading files from the hosts to recover artifacts,
etc, from the actions.
''',
)
def download():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


download.add_command(origin_artifacts)
