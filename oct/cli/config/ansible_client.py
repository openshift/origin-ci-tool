# coding=utf-8
from __future__ import absolute_import, division, print_function

from .generic import configuration_options, update_configuration_option


def get_container_from_context(context):
    """
    Get the container from the Click context.

    :param context: Click context
    :return: configuration container to work on
    """
    return context.obj.ansible_client_configuration


@configuration_options(
    name='ansible-client',
    container='Ansible client',
    use='execute Ansible actions',
    example_key='custom_module_path',
    example_value='/some/path',
    fetch_func=get_container_from_context
)
def ansible_client_command(context, option, value, view):
    """
    Update a setting in the Ansible client configuration file.

    :param context: Click context
    :param option: name of the option to update
    :param value: value to update to
    """
    update_configuration_option(
        container=context.obj.ansible_client_configuration,
        option=option,
        value=value,
        write_func=context.obj.write_ansible_client_configuration
    )
