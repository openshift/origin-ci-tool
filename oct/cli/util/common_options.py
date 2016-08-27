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
