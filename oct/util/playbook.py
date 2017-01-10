# coding=utf-8
"""
A utility module for working with playbooks in the `origin-ci-tool` repository.
"""
from __future__ import absolute_import, division, print_function

from os.path import abspath, dirname, exists, join

from click import ClickException


def playbook_path(playbook_name):
    """
    Get the path to the named playbook. To allow for
    as much brevity as possible in the given playbook
    name, we will attempt to search under:
      - oct/playbooks
      - openshift-ansible/playbooks

    :param playbook_name: the name of the playbook
    :type playbook_name: str

    :return: the path to the playbook
    :rtype: str

    :raises ClickException: when no playbook is found
    """
    from ..oct import __file__ as root_path

    for parent_repo in ['oct', 'openshift-ansible']:
        playbook_file = join(abspath(dirname(root_path)), 'ansible', parent_repo, 'playbooks', playbook_name + '.yml')
        if exists(playbook_file):
            return playbook_file

    raise ClickException('No playbook named {} found!'.format(playbook_name))
