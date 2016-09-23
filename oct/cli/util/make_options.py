# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Path, argument, option


def make_options(func):
    """
    Add all of the make options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    makefile_options = [
        make_target_argument,
        make_parameter_option,
        make_directory_override_option
    ]

    for make_option in reversed(makefile_options):
        func = make_option(func)

    return func


def make_target_argument(func):
    """
    Add the make target argument to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return argument(
        'target',
        nargs=-1,
        required=True
    )(func)


def make_parameter_option(func):
    """
    Add the make parameter option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--env', '-e',
        'parameters',
        metavar='KEY=VAL',
        multiple=True,
        help='Parameter key-value-pair.'
    )(func)


def make_directory_override_option(func):
    """
    Add the make destination option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--dest', '-d',
        'make_destination',
        type=Path(
            file_okay=False
        ),
        help='Remote directory to run make in. Optional.'
    )(func)
