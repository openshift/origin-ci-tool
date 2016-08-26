import config


def default_vars(vars):
    """
    Default unset values in variables using values loaded from
    on-disk configuration.

    :param vars: partially-filled Ansible variables
    :return: defaulted Ansible variables
    """
    if not vars:
        vars = dict()

    if 'origin_ci_hosts' not in vars:
        vars['origin_ci_hosts'] = config._config['hosts']

    if 'origin_ci_connection' not in vars:
        vars['origin_ci_connection'] = config._config['connection']

    if 'origin_ci_become' not in vars:
        vars['origin_ci_become'] = config._config['become']

    if 'origin_ci_become_method' not in vars:
        vars['origin_ci_become_method'] = config._config['become_method']

    if 'origin_ci_become_user' not in vars:
        vars['origin_ci_become_user'] = config._config['become_user']

    return vars
