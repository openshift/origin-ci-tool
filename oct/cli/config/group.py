# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .ansible_client import ansible_client_command
from .ansible_defaults import ansible_defaults_command
from .aws_client import aws_client_command
from .aws_defaults import aws_defaults_command


@group(
    short_help='View, update and append to the serialized configuration.',
    help='''
Common configuration options for clients used by this tool are stored
in serialized form per-user on the file system of this host. These
files should not be edited by hand; rather, they should be viewed and
updated using these command-line endpoints.
''',
)
def configure():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


configure.add_command(ansible_client_command)
configure.add_command(ansible_defaults_command)
configure.add_command(aws_client_command)
configure.add_command(aws_defaults_command)
