# coding=utf-8
from __future__ import absolute_import, division, print_function

from .generic import configuration_options, update_configuration_option


def get_container_from_context(context):
    """
    Get the container from the Click context.

    :param context: Click context
    :return: configuration container to work on
    """
    return context.obj.ansible_variables


@configuration_options(
    name='ansible-defaults',
    container='Ansible default',
    use='parameterize Ansible actions',
    example_key='become_method',
    example_value='pfexec',
    fetch_func=get_container_from_context,
)
def ansible_defaults_command(context, option, value, view):
    """
    Update a setting in the Ansible variables configuration file.

    :param context: Click context
    :param option: name of the option to update
    :param value: value to update to
    """
    update_configuration_option(
        container=context.obj.ansible_variables,
        option=option,
        value=value,
    )
