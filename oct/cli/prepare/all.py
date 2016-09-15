import click
from cli.prepare.docker import docker_version_for_preset
from cli.prepare.golang import golang_version_for_preset
from cli.util.common_options import ansible_output_options
from cli.util.preset_option import preset_option, Preset
from util.playbook import playbook_path
from util.playbook_runner import PlaybookRunner


def install_dependencies_for_preset(ctx, param, value=Preset.origin_master):
    """
    Installs the full set of dependencies on the remote host.

    Handles the special `--for` option, defaults to `origin/master` if
    a preset is not provided by the user.
    """
    if not value or ctx.resilient_parsing:
        return

    prepare_all(value)
    ctx.exit()


_short_help = 'Install dependencies on remote hosts.'


@click.command(
    short_help=_short_help,
    help=_short_help + '''

If a preset is chosen, default values for the other options are used
and user-provided options are ignored.

\b
Examples:
  Install dependencies for the default configuration
  $ oct prepare all
\b
  Install dependencies for a specific version of OpenShift
  $ oct prepare all --for=ose/enterprise-3.3
'''
)
@preset_option(
    help_action='Install dependencies',
    callback=install_dependencies_for_preset
)
@ansible_output_options
def all(preset):
    """
    Installs the full set of dependencies on the remote host.

    :param preset: version of OpenShift for which to install dependencies
    """
    prepare_all(preset)


def prepare_all(preset):
    """
    Installs the full set of dependencies on the remote host.

    :param preset: version of OpenShift for which to install dependencies
    """
    vars = dict(
        origin_ci_docker_package='docker-' + docker_version_for_preset(preset),
        origin_ci_golang_package='golang-' + golang_version_for_preset(preset)
    )

    PlaybookRunner().run(
        playbook_source=playbook_path('prepare/main'),
        vars=vars
    )
