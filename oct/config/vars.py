from . import _config


# use a tuple, not a list
_config_var_fields = [
    'hosts',
    'connection',
    'become',
    'become_method',
    'become_user',
    'docker_volume_group'
]


def default_vars(vars):
    """
    Default unset values in variables using values loaded from
    on-disk configuration.

    :param vars: partially-filled Ansible variables
    :return: defaulted Ansible variables
    """
    if not vars:  # if vars is None
        vars = dict()

    for field in _config_var_fields:
        var = 'origin_ci_' + field
        if var not in vars:
            vars[var] = _config[field]

    vars['origin_ci_user'] = _config['become_user']

    return vars
