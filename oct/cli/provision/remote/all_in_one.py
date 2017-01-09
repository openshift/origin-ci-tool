# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Choice, ClickException, command, option, pass_context

from ..common_options import discrete_ssh_config_option
from ...util.common_options import ansible_output_options


class OperatingSystem(object):
    """
    An enumeration of supported operating systems for
    Vagrant provisioning of VMs.
    """
    fedora = 'fedora'
    centos = 'centos'
    rhel = 'rhel'


class Provider(object):
    """
    An enumeration of supported clouds for provisioning
    of VMs.
    """
    aws = 'aws'


class Stage(object):
    """
    An enumeration of supported stages for images used
    for provisioning of VMs.
    """
    bare = 'bare'
    base = 'base'
    install = 'install'


def destroy_callback(context, _, value):
    """
    Tear down the currently running VM

    :param context: Click context
    :param _: command-line parameter
    :param value: whether or not to tear down the VM
    """
    if not value or context.resilient_parsing:
        return

    destroy(context.obj)
    context.exit()


_short_help = 'Provision a virtual host for an All-In-One deployment.'


@command(
    name='all-in-one',
    short_help=_short_help,
    help=_short_help + '''

An All-In-One deployment of OpenShift uses one virtual host on which
all cluster components are provisioned. These types of deployments are
most useful for short-term development work-flows.

\b
Examples:
  Provision a VM with default parameters (fedora, aws, install)
  $ oct provision remote all-in-one
\b
  Provision a VM with custom parameters
  $ oct provision remote all-in-one --os=centos --provider=aws --stage=base
\b
  Tear down the currently running VMs
  $ oct provision remote all-in-one --destroy
'''
)
@option(
    '--os', '-o',
    'operating_system',
    type=Choice([
        OperatingSystem.fedora,
        OperatingSystem.centos,
        OperatingSystem.rhel
    ]),
    default=OperatingSystem.fedora,
    show_default=True,
    metavar='NAME',
    help='VM operating system.'
)
@option(
    '--provider', '-p',
    type=Choice([
        Provider.aws
    ]),
    default=Provider.aws,
    show_default=True,
    metavar='NAME',
    help='Cloud provider.'
)
@option(
    '--stage', '-s',
    type=Choice([
        Stage.bare,
        Stage.base,
        Stage.install
    ]),
    default=Stage.install,
    show_default=True,
    metavar='NAME',
    help='VM image stage.'
)
@option(
    '--name', '-n',
    metavar='NAME',
    required=True,
    help='VM instance name.'
)
@option(
    '--destroy', '-d',
    is_flag=True,
    expose_value=False,
    help='Tear down the current VMs.',
    callback=destroy_callback
)
@discrete_ssh_config_option
@ansible_output_options
@pass_context
def all_in_one_command(context, operating_system, provider, stage, name, discrete_ssh_config):
    """
    Provision a virtual host for an All-In-One deployment.

    :param context: Click context
    :param operating_system: operating system to use for the VM
    :param provider: provider to use with Vagrant
    :param stage: image stage to base the VM off of
    :param name: name to give to the VM instance
    :param discrete_ssh_config: whether to update ~/.ssh/config or write a new file
    """
    configuration = context.obj
    if provider == Provider.aws:
        provision_with_aws(configuration, operating_system, stage, name, discrete_ssh_config)


def destroy(configuration):
    """
    Tear down the currently running VMs.

    :param configuration: Origin CI Tool configuration
    """
    configuration.run_playbook(
        playbook_relative_path='provision/aws_all_in_one_down'
    )


def provision_with_aws(configuration, operating_system, stage, name, discrete_ssh_config):
    """
    Provision a VM in the cloud using AWS EC2.

    :param configuration: Origin CI tool configuration
    :param operating_system: operating system used for the VM
    :param stage: image stage the VM was based off of
    :param name: name to give to the VM instance
    :param discrete_ssh_config: whether to update ~/.ssh/config or write a new file
    """
    if not configuration.aws_client_configuration.keypair_name:
        raise ClickException(
            'No key-pair name found! Configure one using:\n  $ oct configure aws-client keypair_name NAME'
        )
    if not configuration.aws_client_configuration.private_key_path:
        raise ClickException(
            'No private key path found! Configure one using:\n  $ oct configure aws-client private_key_path PATH'
        )

    configuration.run_playbook(
        playbook_relative_path='provision/aws-up',
        playbook_variables={
            'origin_ci_aws_hostname': configuration.next_available_vagrant_name,  # TODO: fix this
            'origin_ci_aws_ami_os': operating_system,
            'origin_ci_aws_ami_stage': stage,
            'origin_ci_aws_instance_name': name,
            'origin_ci_inventory_dir': configuration.ansible_client_configuration.host_list,
            'origin_ci_aws_keypair_name': configuration.aws_client_configuration.keypair_name,
            'origin_ci_aws_private_key_path': configuration.aws_client_configuration.private_key_path,
            'origin_ci_ssh_config_strategy': 'discrete' if discrete_ssh_config else 'update'
        }
    )

    if stage == Stage.bare:
        # once we have the new host, we must partition the space on it
        # that was set aside for Docker storage, then update the kernel
        # partition tables and set up the volume group backed by the LVM
        # pool
        configuration.run_playbook(
            playbook_relative_path='provision/aws-docker-storage'
        )
