# coding=utf-8
from __future__ import absolute_import, division, print_function

from ansible import constants
from click import option

from ...config import CONFIG


def ansible_output_options(func):
    """
    Add all of the Ansible output options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    output_options = [
        ansible_verbosity_option,
        ansible_dry_run_option,
        ansible_debug_mode_option
    ]

    for output_option in reversed(output_options):
        func = output_option(func)

    return func


def update_ansible_verbosity(ctx, _, value):
    """
    Update the desired Ansible verbosity level.

    :param ctx: Click context
    :param _: command-line parameter
    :param value: desired Ansible verbosity level
    """
    if not value or ctx.resilient_parsing:
        return

    CONFIG['config']['verbosity'] = value


def ansible_verbosity_option(func):
    """
    Add the Ansible verbosity option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--verbose', '-v',
        default=1,
        count=True,
        expose_value=False,
        help='Ansible verbosity level. Repeat to increase.',
        callback=update_ansible_verbosity,
        is_eager=True
    )(func)


def update_ansible_dry_run(ctx, _, value):
    """
    Updated Ansible to do a dry run.

    :param ctx: Click context
    :param _: command-line parameter
    :param value: whether or not to do a dry run
    """
    if not value or ctx.resilient_parsing:
        return

    CONFIG['config']['check'] = True


def ansible_dry_run_option(func):
    """
    Add the Ansible dry run option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--dry-run', '--check', '-C',
        is_flag=True,
        expose_value=False,
        help='Toggle Ansible dry-run mode.',
        callback=update_ansible_dry_run,
        is_eager=True
    )(func)


def update_ansible_debug_mode(ctx, _, value):
    """
    Updated Ansible to run with debug mode on.

    :param ctx: Click context
    :param _: command-line parameter
    :param value: whether or not to turn on debug mode
    """
    if not value or ctx.resilient_parsing:
        return

    constants.DEFAULT_DEBUG = True


def ansible_debug_mode_option(func):
    """
    Add the Ansible debug mode option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--debug', '-d',
        is_flag=True,
        expose_value=False,
        help='Toggle Ansible debug mode.',
        callback=update_ansible_debug_mode,
        is_eager=True
    )(func)
