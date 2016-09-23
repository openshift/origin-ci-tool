# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .remove import remove
from .set import set_command
from .show import show


@group(
    short_help='View, update and append to the serialized configuration.',
    help='''
Common configuration options for Ansible are stored in serialized
form per-user on the file system of the controlling host. These
files should not be edited by hand; rather, they should be viewed
and updated using these command-line endpoints.
'''
)
def config():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


config.add_command(remove)
config.add_command(set_command)
config.add_command(show)
