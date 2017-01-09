# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import ClickException, echo, option

from ..provision.local.all_in_one import Stage


def package_options(func):
    """
    Add all of the package options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--update/--upgrade', '-d/-g',
        'update_current_stage',
        default=False,
        help='Update stage or upgrade to next stage.  [default: upgrade]',
    )(func)


def next_stage(current_stage):
    """
    Determine the VM stage that occurs after the given stage.

    :param current_stage: current VM stage
    :return: next VM stage
    """
    if current_stage == Stage.bare:
        return Stage.base
    elif current_stage == Stage.base:
        return Stage.install
    elif current_stage == Stage.install:
        echo('Warning: No next stage exists past the "{}" stage. Overwriting current stage instead.'.format(Stage.install))
        return Stage.install
    else:
        raise ClickException('The current stage of the VM, "{}", has no next stage specified.'.format(current_stage))
