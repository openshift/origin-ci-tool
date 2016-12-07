# coding=utf-8
from __future__ import absolute_import, division, print_function

from .generic import configuration_options, update_configuration_option


def get_container_from_context(context):
    """
    Get the container from the Click context.

    :param context: Click context
    :return: configuration container to work on
    """
    return context.obj.aws_client_configuration


@configuration_options(
    name='aws-client',
    container='AWS client',
    use='execute AWS EC2 actions',
    example_key='aws_keypair_name',
    example_value='id_rsa',
    fetch_func=get_container_from_context
)
def aws_client_command(context, option, value, view):
    """
    Update a setting in the AWS client configuration file.

    :param context: Click context
    :param option: name of the option to update
    :param value: value to update to
    """
    update_configuration_option(
        container=context.obj.aws_client_configuration,
        option=option,
        value=value,
        write_func=context.obj.write_aws_client_configuration
    )
