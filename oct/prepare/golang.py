import click
from prepare.role_runner import RoleRunner


def install_golang_custom_callback(ctx, param, value):
    """
    Handles the eager `--for` option.
    """
    if not value or ctx.resilient_parsing:
        return

    install_golang_for_preset(value)
    ctx.exit()


@click.command(
    short_help='Install Golang on remote hosts.'
)
@click.option(
    '--version', '-v',
    help='Version of Golang to install.'
)
@click.option(
    '--repo', '-r',
    'repos',
    multiple=True,
    help='Name of a repository to enable when installing Golang.'
)
@click.option(
    '--repourl', '-u',
    'repourls',
    multiple=True,
    help='URL of a repository to register temporarily when installing Golang.'
)
@click.option(
    '--for', '-f',
    'preset',
    type=click.Choice(['origin/master', 'ose/master', 'ose/enterprise-3.2', 'ose/enterprise-3.3']),
    help='Install Golang using a pre-set configuration for a specific version of OpenShift.',
    callback=install_golang_custom_callback,
    is_eager=True
)
@click.option(
    '--hosts', '-h',
    help='Comma-delimited list of hosts on which to install Golang.',
    default='localhost'  # TODO: this should probably not be here, since we should have an inventory
)
def golang(version, repos, repourls, preset, hosts):
    """
    Installs the Go toolchain and source on the remote host.

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
    $ oct prepare golang --version=1.6.2 --repourl=myrepo.com/golang/x86_64/
    """
    install_golang_custom(version, repos, repourls, hosts)


def install_golang_for_preset(preset):
    """
    Install Go on the remote host for a given OpenShift version.

    :param preset: version of OpenShift for which to install Golang
    """
    if preset in ['origin/master', 'ose/master', 'ose/enterprise-3.3', 'ose/enterprise-3.2']:
        install_golang_custom(version='1.6.2')
    else:
        raise click.UsageError('No Golang preset found for OpenShift version: %s' % preset)


def install_golang_custom(version, repos=None, repourls=None, hosts=None):
    """
    Install Go on the remote host.

    :param version: version of Golang to install
    :param repos: list of RPM repositories from which to install Golang
    :param repourls: list of RPM repository URLs from which to install Golang
    """
    role_vars = dict(
        origin_ci_isolated_package='golang'
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
        name='Install Golang',
        role='oct/prepare/roles/isolated-install',
        vars=role_vars,
        hosts=hosts
    )
    runner.run()
