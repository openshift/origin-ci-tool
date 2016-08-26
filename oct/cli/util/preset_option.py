import click


class Preset:
    """
    An enumeration of OpenShift versions that are acceptable
    for presets used by this CLI. Not using the Python Enum
    built-in for python-2.7 compatibility.

    """
    origin_master = 'origin/master'
    ose_master = 'ose/master'
    ose_32 = 'ose/enterprise-3.2'
    ose_321 = 'ose/enterprise-3.2.1'
    ose_33 = 'ose/enterprise-3.3'


def raw_preset_option(help_action, callback):
    """
    Get an option for OpenShift version presets.

    :param help_action: the helptext for the preset option
    :param callback: the callback for the preset option
    :return: the preset option
    """
    return click.option(
        '--for', '-f',
        'preset',
        type=click.Choice([
            Preset.origin_master,
            Preset.ose_master,
            Preset.ose_32,
            Preset.ose_321,
            Preset.ose_33
        ]),
        help=help_action + ' using a pre-set configuration for a specific version of OpenShift.',
        callback=callback,
        is_eager=True
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
