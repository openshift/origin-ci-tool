import config

_config_var_fields = [
    'hosts',
    'connection',
    'become',
    'become_method',
    'become_user'
]


def default_vars(vars):
    """
    Default unset values in variables using values loaded from
    on-disk configuration.

    :param vars: partially-filled Ansible variables
    :return: defaulted Ansible variables
    """
    if not vars:
        vars = dict()

    for field in _config_var_fields:
        var = 'origin_ci_' + field
        if var not in vars:
            vars[var] = config._config[field]

    return vars
