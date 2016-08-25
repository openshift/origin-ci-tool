import click
from prepare.role_runner import RoleRunner


def install_docker_custom_callback(ctx, param, value):
    """
    Handles the eager `--for` option.
    """
    if not value or ctx.resilient_parsing:
        return

    install_docker_for_preset(value)
    ctx.exit()


@click.command(
    short_help='Install Docker on remote hosts.'
)
@click.option(
    '--version', '-v',
    help='Version of Docker to install.'
)
@click.option(
    '--repo', '-r',
    'repos',
    multiple=True,
    help='Name of a repository to enable when installing Docker.'
)
@click.option(
    '--repourl', '-u',
    'repourls',
    multiple=True,
    help='URL of a repository to register temporarily when installing Docker.'
)
@click.option(
    '--for', '-f',
    'preset',
    type=click.Choice(['origin/master', 'ose/master', 'ose/enterprise-3.2', 'ose/enterprise-3.2.1', 'ose/enterprise-3.3']),
    help='Install Docker using a pre-set configuration for a specific version of OpenShift.',
    callback=install_docker_custom_callback,
    is_eager=True
)
@click.option(
    '--hosts', '-h',
    help='Comma-delimited list of hosts on which to install Docker.',
    default='localhost'  # TODO: this should probably not be here, since we should have an inventory
)
def docker(version, repos, repourls, preset, hosts):
    """
    Installs the Docker daemon and CLI on the remote host.

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
    """
    install_docker_custom(version, repos, repourls, hosts)


def install_docker_for_preset(preset):
    """
    Install Docker on the remote host for a given OpenShift version.

    :param preset: version of OpenShift for which to install Docker
    """
    if preset in ['origin/master', 'ose/master', 'ose/enterprise-3.3', 'ose/enterprise-3.2.1']:
        install_docker_custom(version='1.10.3')
    if preset in ['ose/enterprise-3.2']:
        install_docker_custom(version='1.9.1')
    else:
        raise click.UsageError('No Docker preset found for OpenShift version: %s' % preset)


def install_docker_custom(version, repos=None, repourls=None, hosts=None):
    """
    Install Docker on the remote host.

    :param version: version of Docker to install
    :param repos: list of RPM repositories from which to install Docker
    :param repourls: list of RPM repository URLs from which to install Docker
    """
    role_vars = dict(
        origin_ci_isolated_package='docker'
    )

    if version:
        role_vars['origin_ci_isolated_package'] += '-' + version

    if repos:
        role_vars['origin_ci_isolated_disabledrepos'] = '*'
        role_vars['origin_ci_isolated_enabledrepos'] = ','.join(repos)

    if repourls:
        role_vars['origin_ci_isolated_tmp_repourls'] = repourls

    runner = RoleRunner()
    runner.add_role(
        name='Install Docker',
        role='oct/prepare/roles/isolated-install',
        vars=role_vars,
        hosts=hosts
    )
    runner.add_role(
        name='Configure Docker',
        role='oct/prepare/roles/docker',
        hosts=hosts
    )
    runner.run()
