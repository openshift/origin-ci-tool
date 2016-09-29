# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import UsageError, command, pass_context

from ..prepare.isolated_install_options import isolated_install_options
from ..util.common_options import ansible_output_options
from ..util.preset_option import Preset


def install_docker_for_preset(context, _, value):
    """
    Install Docker on the remote host for a given OpenShift version.
    Handles the special `--for` option.

    :param context: Click context
    :param _: command-line parameter
    :param value: version of OpenShift for which to install Docker
    """
    if not value or context.resilient_parsing:
        return

    install_docker(client=context.obj, version=docker_version_for_preset(value))
    context.exit()


def docker_version_for_preset(preset):
    """
    Determine the Docker version for a given preset.

    :param preset: version of OpenShift for which to install Docker
    :return: the Docker version to install
    """
    # Maybe make this functionality as class methods on Preset?
    if preset in [Preset.origin_master, Preset.ose_master, Preset.ose_33, Preset.ose_321]:
        return '1.10.3'
    if preset in [Preset.ose_32]:
        return '1.9.1'
    else:
        raise UsageError('No Docker preset found for OpenShift version: %s' % preset)


_short_help = 'Install Docker on remote hosts.'


@command(
    short_help=_short_help,
    help=_short_help + '''

The Docker install can be parameterized with the Docker package
version that is required, as well as the existing RPM repositories
and new RPM repositories from the web to enable when installing it.

If repositories or repository URLs are given, they will be the only
repositories enabled when the Docker install occurs. Any repositories
created from repository URLs will be registered only for the Docker
install and will be removed after the fact.

If a preset is chosen, default values for the other options are used
and user-provided options are ignored.

\b
Examples:
  Install Docker for a specific version of OpenShift
  $ oct prepare docker --for=ose/enterprise-3.3
\b
  Install a specific Docker version present in default RPM repositories
  $ oct prepare docker --version=1.9.1
\b
  Install a specific Docker version from an available custom RPM repository
  $ oct prepare docker --version=1.10.3 --repo=my-custom-docker-repo
\b
  Install a specific Docker version from an RPM repository available on the web
  $ oct prepare docker --version=1.11.0 --repourl=myrepo.com/docker/x86_64/
'''
)
@isolated_install_options(
    package_name='Docker',
    preset_callback=install_docker_for_preset
)
@ansible_output_options
@pass_context
def docker(context, version, repos, repourls):
    """
    Installs the Docker daemon and CLI on the remote host.

    :param context: Click context
    :param version: version of Docker to install
    :param repos: list of RPM repositories from which to install Docker
    :param repourls: list of RPM repository URLs from which to install Docker
    """
    install_docker(context.obj, version, repos, repourls)


def install_docker(client, version, repos=None, repourls=None):
    """
    Install Docker on the remote host.

    :param client: Ansible client
    :param version: version of Docker to install
    :param repos: list of RPM repositories from which to install Docker
    :param repourls: list of RPM repository URLs from which to install Docker
    """
    playbook_variables = {}

    if version:
        playbook_variables['origin_ci_docker_version'] = version

    if repos:
        playbook_variables['origin_ci_docker_disabledrepos'] = '*'
        playbook_variables['origin_ci_docker_enabledrepos'] = ','.join(repos)

    if repourls:
        playbook_variables['origin_ci_docker_tmp_repourls'] = list(repourls)

    client.run_playbook(
        playbook_relative_path='prepare/docker',
        playbook_variables=playbook_variables
    )
