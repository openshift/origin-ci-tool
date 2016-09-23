from __future__ import absolute_import, division, print_function

from click import Choice, option

class Preset:
from .repository_options import Repository


    """
    An enumeration of OpenShift versions that are acceptable
    for presets used by this CLI. Not using the Python Enum
    built-in for python-2.7 compatibility.

    """
    origin_master = Repository.origin + '/master'
    ose_master = Repository.enterprise + '/master'
    ose_32 = Repository.enterprise + '/enterprise-3.2'
    ose_321 = Repository.enterprise + '/enterprise-3.2.1'
    ose_33 = Repository.enterprise + '/enterprise-3.3'


def raw_preset_option(help_action, callback):
    """
    Get an option for OpenShift version presets.

    :param help_action: the helptext for the preset option
    :param callback: the callback for the preset option
    :return: the preset option
    """
    return option(
        '--for', '-f',
        'preset',
        type=Choice([
            Preset.origin_master,
            Preset.ose_master,
            Preset.ose_32,
            Preset.ose_321,
            Preset.ose_33
        ]),
        metavar='PRESET',
        help=help_action + ' using a pre-set configuration for a specific version of OpenShift.',
        callback=callback
    )


def preset_option(help_action, callback):
    """
    Get a decorator for an OpenShift version preset option.

    :param help_action: the helptext for the preset option
    :param callback: the callback for the preset option
    :return: the preset option decorator
    """

    def preset_option_decorator(func):
        return raw_preset_option(help_action, callback)(func)

    return preset_option_decorator
