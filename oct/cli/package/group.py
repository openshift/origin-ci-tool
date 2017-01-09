# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .aws import ami
from .vagrant import vagrant


@group(
    short_help='Package a running virtual machine into a redistributable image.',
    help='''
Once a remote host has been subjected to Ansible actions, it
is often useful to package the resulting machine into an image
that can be redistributed so others do not have to re-do the
work. This command allows for packaging images from running
remote hosts; however, it requires host dependencies for local
virtual machine packaging.
''',
)
def package():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


package.add_command(vagrant)
package.add_command(ami)
