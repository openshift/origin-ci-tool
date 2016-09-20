from . import _config_path, _inventory_path


# Using a dict is probably fine for now, but you may want a class for this later
def default_config():
    """
    Generate a default configuration.

    :return: the default configuration dictionary
    """
    return dict(
        config_path=_config_path,
        host_list=_inventory_path,
        # hosts are the hosts we want to run plays on
        hosts='vms',
        connection='ssh',
        verbosity=1,
        module_path=None,
        forks=5,
        vm_hostname='openshiftdevel',
        docker_volume_group='docker',
        become=True,
        become_method='sudo',
        become_user='origin',
        check=False
    )


def default_inventory():
    """
    Generate a default inventory, formatted for serialization.

    :return: the default inventory
    """
    return """
localhost

[vms]
"""
