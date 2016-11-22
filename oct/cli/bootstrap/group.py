# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .host import host
from .node import node
from .self import self


@group(
    short_help='Get a machine ready to be an Ansible node or target host.',
    help='''
In order for Ansible to interact with a target host, or for a machine
to be used as a node that issues Ansible directives, specific dependencies
exist. These commands allow for a machine to be boot-strapped into an
Ansible target host or an Ansible node.
'''
)
def bootstrap():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


bootstrap.add_command(host)
bootstrap.add_command(node)
bootstrap.add_command(self)
