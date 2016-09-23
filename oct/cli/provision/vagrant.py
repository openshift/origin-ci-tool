from __future__ import absolute_import, division, print_function

from click import Choice, UsageError, command, option

from ..util.common_options import ansible_output_options
from ...config import CONFIG
from ...config.load import add_host_to_inventory, remove_host_from_inventory, safe_update_config
from ...util.playbook import playbook_path
from ...util.playbook_runner import PlaybookRunner


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


def destroy_callback(ctx, param, value):
    """
    Tear down the currently running VM using `vagrant destroy`

    :param value: whether or not to tear down the VM
    """
    if not value or ctx.resilient_parsing:
        return

    destroy()
    ctx.exit()


_short_help = 'Provision a local VM using Vagrant.'


@command(
    short_help=_short_help,
    help=_short_help + '''

Local VM provisioning is supported for a range of operating systems,
virtualization providers, and image stages. The choice of operating
system and virtualiztion provider allows for flexibility, but it is
the intention that all combinations have parity, so the choice should
not impact your workload.

Note: without a license to publish and distribute VMWare Fusion box
files, we cannot provide any image stage other than the most basic
bare operating system stage. If you are using VMWare Fusion as your
Vagrant provider, you must build the other image stages yourself.

\b
Examples:
  Provision a VM with default parameters (fedora, libvirt, install)
  $ oct provision vagrant
\b
  Remove the current VM
  $ oct provision vagrant --destroy
\b
  Provision a VM with custom parameters
  $ oct provision vagrant --os=centos --provider=virtualbox --stage=base
\b
  Tear down the currently running VM
  $ oct provision vagrant --destroy
\b
  Provision a VM with a specific IP address
  $ oct provision vagrant --ip=10.245.2.2
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
    default='10.245.2.2',
    show_default=True,
    metavar='ADDRESS',
    help='Desired IP of the VM.'
)
@option(
    '--destroy', '-d',
    is_flag=True,
    expose_value=False,
    help='Tear down the current VM.',
    callback=destroy_callback
)
@ansible_output_options
def vagrant(operating_system, provider, stage, ip):
    """
    Provision a local VM using Vagrant.

    :param operating_system: operating system to use for the VM
    :param provider: provider to use with Vagrant
    :param stage: image stage to base the VM off of
    :param ip: desired VM IP address
    """
    validate(provider, stage)
    provision(operating_system, provider, stage, ip)


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


def provision(operating_system, provider, stage, ip):
    """
    Provision a local VM using Vagrant.

    :param operating_system: operating system to use for the VM
    :param provider: provider to use with Vagrant
    :param stage: image stage to base the VM off of
    :param ip: desired VM IP address
    """
    PlaybookRunner().run(
        playbook_source=playbook_path('provision/vagrant-up'),
        playbook_variables={
            'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
            'origin_ci_vagrant_os': operating_system,
            'origin_ci_vagrant_provider': provider,
            'origin_ci_vagrant_stage': stage,
            'origin_ci_vagrant_ip': ip,
            'origin_ci_vagrant_hostname': CONFIG['config']['vm_hostname']
        }
    )

    # if we successfully executed the playbook, we have a new host
    add_host_to_inventory(CONFIG['config']['vm_hostname'])
    CONFIG['config']['vm'] = {
        'operating_system': operating_system,
        'provider': provider,
        'stage': stage
    }
    safe_update_config()

    if stage == Stage.bare:
        # once we have the new host, we must partition the space on it
        # that was set aside for Docker storage, then power cycle it to
        # update the kernel partition tables, then set up the volume
        # group backed by the LVM pool
        PlaybookRunner().run(
            playbook_source=playbook_path('provision/vagrant-docker-storage'),
            playbook_variables={
                'origin_ci_vagrant_provider': provider,
                'origin_ci_vagrant_home_dir': CONFIG['vagrant_home'],
                'origin_ci_vagrant_hostname': CONFIG['config']['vm_hostname']
            }
        )


def destroy():
    """
    Tear down the currently running Vagrant VM.
    """
    PlaybookRunner().run(
        playbook_source=playbook_path('provision/vagrant-down'),
        playbook_variables={
            'origin_ci_vagrant_home_dir': CONFIG['vagrant_home']
        }
    )

    # if we successfully executed the playbook, we have removed a host
    remove_host_from_inventory(CONFIG['config']['vm_hostname'])
    if 'vm' in CONFIG['config']:
        CONFIG['config'].pop('vm')
    safe_update_config()
