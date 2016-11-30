# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Choice, UsageError, command, option, pass_context

from ..util.common_options import ansible_output_options
from ...config.vagrant import VagrantVMMetadata

DEFAULT_MASTER_IP = '10.245.2.2'


class OperatingSystem(object):
    """
    An enumeration of supported operating systems for
    Vagrant provisioning of local VMs.
    """
    fedora = 'fedora'
    centos = 'centos'


class Provider(object):
    """
    An enumeration of supported virtualization providers
    for provisioning of local VMs.
    """
    libvirt = 'libvirt'
    virtualbox = 'virtualbox'
    vmware = 'vmware_fusion'


class Stage(object):
    """
    An enumeration of supported stages for boxes used
    for Vagrant provisioning of local VMs.
    """
    bare = 'bare'
    base = 'base'
    install = 'install'


def destroy_callback(context, _, value):
    """
    Tear down the currently running VM using `vagrant destroy`

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

Local VM provisioning is supported for a range of operating systems,
virtualization providers, and image stages. The choice of operating
system and virtualization provider allows for flexibility, but it is
the intention that all combinations have parity, so the choice should
not impact your workload.

Note: without a license to publish and distribute VMWare Fusion box
files, we cannot provide any image stage other than the most basic
bare operating system stage. If you are using VMWare Fusion as your
Vagrant provider, you must build the other image stages yourself.

\b
Examples:
  Provision a VM with default parameters (fedora, libvirt, install)
  $ oct provision_with_vagrant all-in-one
\b
  Provision a VM with custom parameters
  $ oct provision_with_vagrant all-in-one --os=centos --provider=virtualbox --stage=base
\b
  Tear down the currently running VMs
  $ oct provision_with_vagrant all-in-one --destroy
\b
  Provision a VM with a specific IP address
  $ oct provision_with_vagrant all-in-one --ip=10.245.2.2
'''
)
@option(
    '--os', '-o',
    'operating_system',
    type=Choice([
        OperatingSystem.fedora,
        OperatingSystem.centos
    ]),
    default=OperatingSystem.fedora,
    show_default=True,
    metavar='NAME',
    help='VM operating system.'
)
@option(
    '--provider', '-p',
    type=Choice([
        Provider.libvirt,
        Provider.virtualbox,
        Provider.vmware
    ]),
    default=Provider.libvirt,
    show_default=True,
    metavar='NAME',
    help='Virtualization provider.'
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
    '--master-ip', '-i',
    'ip',
    default=DEFAULT_MASTER_IP,
    show_default=True,
    metavar='ADDRESS',
    help='Desired IP of the VM.'
)
@option(
    '--destroy', '-d',
    is_flag=True,
    expose_value=False,
    help='Tear down the current VMs.',
    callback=destroy_callback
)
@ansible_output_options
@pass_context
def all_in_one(context, operating_system, provider, stage, ip):
    """
    Provision a virtual host for an All-In-One deployment.

    :param context: Click context
    :param operating_system: operating system to use for the VM
    :param provider: provider to use with Vagrant
    :param stage: image stage to base the VM off of
    :param ip: desired VM IP address
    """
    configuration = context.obj
    validate(provider, stage)
    if provider in [Provider.virtualbox, Provider.libvirt, Provider.vmware]:
        provision_with_vagrant(configuration, operating_system, provider, stage, ip)


def validate(provider, stage):
    """
    Validate that the stage requested exists for the provider.
    We do not have a license for posting or distributing any
    VMWare Fusion images, so we cannot provide any stage more
    advanced than the bare OS for this provider.

    :param provider: Vagrant provider chosen
    :param stage: image stage chosen
    """
    if provider == Provider.vmware and stage != Stage.bare:
        raise UsageError('Only the %s stage is supported for the %s provider.' % (Stage.bare, Provider.vmware))


def provision_with_vagrant(configuration, operating_system, provider, stage, ip):
    """
    Provision a local VM using Vagrant.

    :param configuration: Origin CI tool configuration
    :param operating_system: operating system to use for the VM
    :param provider: provider to use with Vagrant
    :param stage: image stage to base the VM off of
    :param ip: desired VM IP address
    """
    hostname = configuration.next_available_vagrant_name
    home_dir = configuration.vagrant_home_directory(hostname)
    configuration.run_playbook(
        playbook_relative_path='provision/vagrant-up',
        playbook_variables={
            'origin_ci_vagrant_home_dir': home_dir,
            'origin_ci_vagrant_os': operating_system,
            'origin_ci_vagrant_provider': provider,
            'origin_ci_vagrant_stage': stage,
            'origin_ci_vagrant_ip': ip,
            'origin_ci_vagrant_hostname': hostname,
            'origin_ci_inventory_dir': configuration.ansible_client_configuration.host_list
        }
    )

    # if we successfully executed the playbook, we have a
    # new host and need to update our metadata and records
    register_host(configuration, home_dir, hostname, operating_system, provider, stage)

    if stage == Stage.bare and provider != Provider.virtualbox:
        # once we have the new host, we must partition the space on it
        # that was set aside for Docker storage, then power cycle it to
        # update the kernel partition tables, then set up the volume
        # group backed by the LVM pool
        # TODO: doing this with VirtualBox breaks Ansible's SSH connection
        # to the machine, re-enable this for the VirtualBox provider once
        # we have figured out how to fix that
        configuration.run_playbook(
            playbook_relative_path='provision/vagrant-docker-storage',
            playbook_variables={
                'origin_ci_vagrant_provider': provider,
                'origin_ci_vagrant_home_dir': home_dir,
                'origin_ci_vagrant_hostname': hostname
            }
        )


def register_host(configuration, home_dir, hostname, operating_system, provider, stage):
    """
    Register a new host by updating metadata records for the
    new VM both in the in-memory cache for this process and
    the on-disk records that will persist past this CLI call.

    :param configuration: Origin CI tool configuration
    :param home_dir: directory from which the VM was created
    :param hostname: hostname of the VM
    :param operating_system: operating system used for the VM
    :param provider: provider used with Vagrant
    :param stage: image stage the VM was based off of
    """
    configuration.register_vagrant_host(VagrantVMMetadata(data={
        'directory': home_dir,
        'hostname': hostname,
        'provisioning_details': {
            'operating_system': operating_system,
            'provider': provider,
            'stage': stage
        },
        # we are supporting an all-in-one deployment with the
        # VM, so this VM will be both a master and a node
        'groups': [
            'masters',
            'nodes'
        ],
        # no `infra` region exists as we need the same node to
        # host OpenShift infrastructure and be schedule-able
        'extra': {
            'openshift_schedulable': True,
            'openshift_node_labels': {
                'region': 'infra',
                'zone': 'default'
            }
        }
    }))


def destroy(configuration):
    """
    Tear down the currently running Vagrant VMs.

    :param configuration: Origin CI Tool configuration
    """
    for vm in configuration.registered_vagrant_machines():
        configuration.run_playbook(
            playbook_relative_path='provision/vagrant-down',
            playbook_variables={
                'origin_ci_vagrant_home_dir': vm.directory,
                'origin_ci_vagrant_hostname': vm.hostname
            }
        )

        # if we successfully executed the playbook, we have removed a host
        vm.remove()
