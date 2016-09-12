import os

import oct

_playbooks_root = os.path.abspath(os.path.dirname(oct.__file__)) + '/ansible/oct/playbooks/'


def playbook_path(playbook_name):
    """
    Get the path to the named playbook.

    :param playbook_name: the name of the playbook
    :return: the path to the playbook
    """
    return _playbooks_root + playbook_name + '.yml'
