# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import ClickException, echo, option, Choice

from ..provision.local.all_in_one import Stage


def package_options(func):
    """
    Add all of the package options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    option(
        '--stage',
        '-s',
        'upgrade_stage',
        type=Choice(['current', 'next', 'fork', 'base']),
        help='Update the current stage, upgrade to next default stage, or choose a stage',
    )(func)
    option(
        '--upgrade',
        '-g',
        'upgrade_current_stage',
        is_flag=True,
        help='[DEPRECATED] Upgrade to next stage.',
    )(func)
    return option(
        '--update',
        '-d',
        'update_current_stage',
        is_flag=True,
        help='[DEPRECATED] Update the current stage.',
    )(func)


def next_stage(current_stage, upgrade_stage):
    """
    Determine the VM stage that occurs after the given stage.

    :param current_stage: current VM stage
    :return: next VM stage
    """
    if upgrade_stage is not None:
        if upgrade_stage is "current":
            return current_stage
        if upgrade_stage is "fork":
            return Stage.fork
        if upgrade_stage is "base":
            return Stage.base

    if current_stage == Stage.bare:
        return Stage.base
    elif current_stage == Stage.base:
        return Stage.build
    elif current_stage == Stage.build:
        return Stage.install
    elif current_stage == Stage.install:
        echo('Warning: No next stage exists past the "{}" stage. Overwriting current stage instead.'.format(Stage.install))
        return Stage.install
    else:
        raise ClickException('The current stage of the VM, "{}", has no next stage specified.'.format(current_stage))
