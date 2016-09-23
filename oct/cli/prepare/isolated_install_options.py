# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import option

from ..util.preset_option import raw_preset_option


def isolated_install_options(package_name, preset_callback):
    """
    Get a decorator for isolated package installation options.

    :param package_name: the name of the package being installed
    :param preset_callback: the callback for the preset option
    :return: the decorator for the CLI function
    """

    def isolated_install_options_decorator(func):
        click_options = [
            option(
                '--version', '-v',
                metavar='VERSION',
                help='Version of ' + package_name + ' to install.'
            ),
            option(
                '--repo', '-r',
                'repos',
                multiple=True,
                metavar='NAME',
                help='Name of a repository to enable when installing ' + package_name + '.'
            ),
            option(
                '--repourl', '-u',
                'repourls',
                multiple=True,
                metavar='URL',
                help='URL of a repository to register temporarily when installing ' + package_name + '.'
            ),
            raw_preset_option(
                help_action='Install ' + package_name,
                callback=preset_callback
            )
        ]

        for click_option in reversed(click_options):
            func = click_option(func)

        return func

    return isolated_install_options_decorator
