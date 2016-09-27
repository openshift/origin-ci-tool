# coding=utf-8
from __future__ import absolute_import, division, print_function

from os.path import abspath, dirname, join


def playbook_path(playbook_name):
    """
    Get the path to the named playbook.

    :param playbook_name: the name of the playbook
    :return: the path to the playbook
    """
    from ..oct import __file__ as root_path
    return join(abspath(dirname(root_path)), 'ansible', 'oct', 'playbooks', playbook_name + '.yml')
