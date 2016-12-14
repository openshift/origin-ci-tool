# coding=utf-8
from __future__ import absolute_import, division, print_function

from ansible.cli import CLI
from click import command, echo

# auto-generated variables
VERSION = '0.1.0'
OPENSHIFT_ANSIBLE_VERSION = 'openshift-ansible-3.4.17-1-148-g134c620'
OPENSHIFT_ANSIBLE_CHECKOUT = '134c6200d1c24131da456808a7b8b7f59a14f91d'

_short_help = 'Print version information for this tool.'


@command(
    short_help=_short_help,
    help=_short_help + '''

As this tool bundles a number of other tools to achieve
its goals, the version of all of those tools is important
to fully define the system.
'''
)
def version():
    """
    Print version information.
    """
    echo('origin-ci-tool version:')
    echo('\toct ' + VERSION + '\n')
    echo('ansible version:')
    echo(''.join(['\t' + line + '\n' for line in CLI.version('ansible').splitlines()]))
    echo('openshift-ansible version:')
    echo('\t{}'.format(OPENSHIFT_ANSIBLE_VERSION))
    echo('\t  master/HEAD at {}\n'.format(OPENSHIFT_ANSIBLE_CHECKOUT))
    echo('openshift-ansible-contrib version:')
    echo('\tTODO')
