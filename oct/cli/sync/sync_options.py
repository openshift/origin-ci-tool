import click
from __future__ import absolute_import, division, print_function


def sync_options(func):
    """
    Add all of the sync options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    options = [
        sync_source_option,
        sync_destination_option
    ]

    for option in reversed(options):
        func = option(func)

    return func


def sync_source_option(func):
    """
    Add the sync source option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--src', '-s',
        'sync_source',
        type=click.Path(
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            readable=True
        ),
        help='Local directory from which to sync. Optional.'
    )(func)


def sync_destination_option(func):
    """
    Add the sync destination option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--dest', '-d',
        'sync_destination',
        type=click.Path(
            file_okay=False,
            dir_okay=True
        ),
        help='Remote directory to sync to. Optional.'
    )(func)
