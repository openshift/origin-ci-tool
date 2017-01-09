# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Path, option


def sync_options(func):
    """
    Add all of the sync options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    all_options = [
        sync_source_option,
        sync_destination_option,
    ]

    for sync_option in reversed(all_options):
        func = sync_option(func)

    return func


def sync_source_option(func):
    """
    Add the sync source option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--src', '-s',
        'sync_source',
        type=Path(
            exists=True,
            file_okay=False,
            resolve_path=True,
        ),
        help='Local directory from which to sync. Optional.',
    )(func)


def sync_destination_option(func):
    """
    Add the sync destination option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--dest', '-d',
        'sync_destination',
        type=Path(
            file_okay=False,
        ),
        help='Remote directory to sync to. Optional.',
    )(func)
