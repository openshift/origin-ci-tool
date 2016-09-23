# coding=utf-8
from __future__ import absolute_import, division, print_function


def default_config(host_list):
    """
    Generate a default configuration.

    :return: the default configuration dictionary
    """
    return {
        'hosts': 'vms',
        'host_list': host_list,
        'connection': 'ssh',
        'verbosity': 1,
        'module_path': None,
        'forks': 5,
        'vm_hostname': 'openshiftdevel',
        'docker_volume_group': 'docker',
        'become': True,
        'become_method': 'sudo',
        'become_user': 'origin',
        'check': False
    }


def default_inventory():
    """
    Generate a default inventory, formatted for serialization.

    :return: the default inventory
    """
    return """
localhost

[vms]
"""
