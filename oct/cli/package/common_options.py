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
    return option(
        '--stage',
        '-s',
        'upgrade_stage',
        type=Choice(['current', 'next', 'fork', 'base', 'crio', 'ose-master', 'ose-ose-enterprise-39', 'ose-ose-enterprise-38', 'ose-ose-enterprise-37', 'ose-ose-enterprise-36']),
        help='Update the current stage, upgrade to next default stage, or choose a stage',
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
        if upgrade_stage is "crio":
            return Stage.crio

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
