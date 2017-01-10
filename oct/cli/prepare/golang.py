# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import UsageError, command, pass_context

from ..prepare.isolated_install_options import isolated_install_options
from ..util.common_options import ansible_output_options
from ..util.preset_option import Preset


def install_golang_custom_callback(context, _, value):
    """
    Install Go on the remote host for a given OpenShift version.
    Handles the special `--for` option.

    :param context: Click context
    :param _: command-line parameter
    :param value: version of OpenShift for which to install Golang
    """
    if not value or context.resilient_parsing:
        return

    install_golang(client=context.obj, version=golang_version_for_preset(value))
    context.exit()


def golang_version_for_preset(preset):
    """
    Determine the Golang version for a given preset.

    :param preset: version of OpenShift for which to install Golang
    :return: the Golang version to install
    """
    if preset in [Preset.origin_master, Preset.ose_master, Preset.ose_32, Preset.ose_321, Preset.ose_33]:
        return '1.6.3'
    else:
        raise UsageError('No Golang preset found for OpenShift version: %s' % preset)


_SHORT_HELP = 'Install Golang on remote hosts.'


@command(
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

The Go install can be parameterized with the Go package version that
is required, as well as the existing RPM repositories and new RPM
repositories from the web to enable when installing it.

If repositories or repository URLs are given, they will be the only
repositories enabled when the Go install occurs. Any repositories
created from repository URLs will be registered only for the Go
install and will be removed after the fact.

If a preset is chosen, default values for the other options are used
and user-provided options are ignored.

\b
Examples:
  Install Go for a specific version of OpenShift
  $ oct prepare golang --for=ose/enterprise-3.3
\b
  Install a specific Go version present in default RPM repositories
  $ oct prepare golang --version=1.4.2
\b
  Install a specific Go version from an available custom RPM repository
  $ oct prepare golang --version=1.5.3 --repo=my-custom-golang-repo
\b
  Install a specific Go version from an RPM repository available on the web
  $ oct prepare golang --version=1.6.3 --repourl=myrepo.com/golang/x86_64/
''',
)
@isolated_install_options(
    package_name='Golang',
    preset_callback=install_golang_custom_callback,
)
@ansible_output_options
@pass_context
def golang(context, version, repos, repourls):
    """
    Installs the Go toolchain and source on the remote host.

    :param context: Click context
    :param version: version of Golang to install
    :param repos: list of RPM repositories from which to install Golang
    :param repourls: list of RPM repository URLs from which to install Golang
    """
    install_golang(context.obj, version, repos, repourls)


def install_golang(client, version, repos=None, repourls=None):
    """
    Install Go on the remote host.

    :param client: Ansible client
    :param version: version of Golang to install
    :param repos: list of RPM repositories from which to install Golang
    :param repourls: list of RPM repository URLs from which to install Golang
    """
    playbook_variables = {}

    if version:
        playbook_variables['origin_ci_golang_version'] = version

    if repos:
        playbook_variables['origin_ci_golang_disabledrepos'] = '*'
        playbook_variables['origin_ci_golang_enabledrepos'] = ','.join(repos)

    if repourls:
        playbook_variables['origin_ci_golang_tmp_repourls'] = list(repourls)

    client.run_playbook(
        playbook_relative_path='prepare/golang',
        playbook_variables=playbook_variables,
    )
