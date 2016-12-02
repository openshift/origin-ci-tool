# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .all_in_one import all_in_one_command

_short_help = 'Provision virtual machines under a local hypervisor.'


@group(
    short_help=_short_help,
    help=_short_help + '''

Local VM provisioning is supported for a range of operating systems,
virtualization providers, and image stages. The choice of operating
system and virtualization provider allows for flexibility, but it is
the intention that all combinations have parity, so the choice should
not impact your workload.

Note: without a license to publish and distribute VMWare Fusion box
files, we cannot provide any image stage other than the most basic
bare operating system stage. If you are using VMWare Fusion as your
Vagrant provider, you must build the other image stages yourself.
'''
)
def local():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


local.add_command(all_in_one_command)
