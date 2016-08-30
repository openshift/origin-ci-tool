import ansible.constants as C
import click
import config


def update_ansible_verbosity(ctx, param, value):
    """
    Update the desired Ansible verbosity level.

    :param value: desired Ansible verbosity level
    """
    if not value or ctx.resilient_parsing:
        return

    config._config['verbosity'] = value


def ansible_verbosity_option(func):
    """
    Add the Ansible verbosity option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--verbose', '-v',
        default=1,
        count=True,
        expose_value=False,
        help='Ansible verbosity level. Repeat to increase.',
        callback=update_ansible_verbosity,
        is_eager=True
    )(func)


def update_ansible_dry_run(ctx, param, value):
    """
    Updated Ansible to do a dry run.

    :param value: whether or not to do a dry run
    """
    if not value or ctx.resilient_parsing:
        return

    config._config['check'] = True


def ansible_dry_run_option(func):
    """
    Add the Ansible dry run option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--dry-run', '--check', '-C',
        is_flag=True,
        expose_value=False,
        help='Toggle Ansible dry run, no changes will be made.',
        callback=update_ansible_dry_run,
        is_eager=True
    )(func)


def update_ansible_debug_mode(ctx, param, value):
    """
    Updated Ansible to run with debug mode on.

    :param value: whether or not to turn on debug mode
    """
    if not value or ctx.resilient_parsing:
        return

    C.DEFAULT_DEBUG = True


def ansible_debug_mode_option(func):
    """
    Add the Ansible debug mode option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--debug', '-d',
        is_flag=True,
        expose_value=False,
        help='Toggle Ansible debug mode.',
        callback=update_ansible_debug_mode,
        is_eager=True
    )(func)
