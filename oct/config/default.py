import config


def default_config():
    """
    Generate a default configuration.

    :return: the default configuration dictionary
    """
    return dict(
        config_path=config._config_path,
        host_list=config._inventory_path,
        # hosts are the hosts we want to run plays on
        hosts='localhost',  # TODO: this default doesn't make sense for anything but testing
        connection='local',  # TODO: same as above
        verbosity=1,
        module_path='',
        forks=5,
        # TODO: are these valid defaults? how do we determine what is useful for local testing versus the tool itself?
        become=True,
        become_method='sudo',
        become_user='root',
        check=False  # TODO: allow users to pass this in (--dry-run)
    )


def default_inventory():
    """
    Generate a default inventory, formatted for serialization.

    :return: the default inventory
    """
    return '\n'.join([
        'localhost'
    ])
