# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

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
def configure():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


configure.add_command(set_command)
configure.add_command(show)
