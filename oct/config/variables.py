# coding=utf-8
from __future__ import absolute_import, division, print_function

from . import CONFIG

_config_var_fields = (
    'hosts',
    'connection',
    'become',
    'become_method',
    'become_user',
    'docker_volume_group'
)


def default_variables(playbook_variables):
    """
    Default unset values in variables using values loaded from
    on-disk configuration.

    :param playbook_variables: partially-filled Ansible variables
    :return: defaulted Ansible variables
    """
    if not playbook_variables:
        playbook_variables = {}

    for field in _config_var_fields:
        var = 'origin_ci_' + field
        if var not in playbook_variables:
            playbook_variables[var] = CONFIG['config'][field]

    playbook_variables['origin_ci_user'] = CONFIG['config']['become_user']

    return playbook_variables
