# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import ClickException
from os.path import abspath, dirname, exists, join


def playbook_path(playbook_name):
    """
    Get the path to the named playbook. To allow for
    as much brevity as possible in the given playbook
    name, we will attempt to search under:
      - oct/playbooks
      - openshift-ansible/playbooks

    :param playbook_name: the name of the playbook
    :return: the path to the playbook
    """
    from ..oct import __file__ as root_path

    for parent_repo in ['oct', 'openshift-ansible']:
        playbook_path = join(abspath(dirname(root_path)), 'ansible', parent_repo, 'playbooks', playbook_name + '.yml')
        if exists(playbook_path):
            return playbook_path

    raise ClickException('No playbook named {} found!'.format(playbook_name))
