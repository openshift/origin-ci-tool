import click
from cli.sync.git_options import git_options, validate_git_specifier, git_version_specifier, git_options_helptext
from cli.sync.sync_options import sync_destination_option
from cli.util.common_options import ansible_output_options
from cli.util.repository_options import repository_argument, Repository
from util.playbook import playbook_path
from util.playbook_runner import PlaybookRunner

_short_help = 'Synchronize a repository using remote servers.'


@click.command(
    short_help=_short_help,
    help=_short_help + '''

Source code repositories on the remote hosts can be updated to
the state held on authoritative upstream Git servers with this
command.

Both the sync destination directory on the remote hosts is
optional if the $GOPATH environment variable is set, as it will
be assumed to be of the following form, where '<REPOSITORY>' is
the single argument accepted by this command:
    $GOPATH/src/github.com/openshift/<REPOSITORY>

''' + git_options_helptext + '''

\b
Examples:
  Synchronize the Origin repo, auto-detecting the location
  $ oct sync remote origin
\b
  Synchronize the Origin repo, specifying a different remote
  $ oct sync remote origin --new-remote myfork https://host/origin.git
\b
  Synchronize the Origin repo, speciyfing a branch on an existing remote
  $ oct sync remote origin --remote=myfork --branch=my-feature-branch
\b
  Synchronize the logging repo, specifying a specific branch
  $ oct sync remote origin-aggregated-logging --branch=enterprise
\b
  Synchronize the Origin repo, specifying a pull request refspec
  $ oct sync remote origin --refspec=/pull/1000/head --branch=pull-1000
'''
)
@repository_argument
@sync_destination_option
@click.option(
    '--remote', '-r',
    metavar='NAME',
    help='Named remote server to use.  [default: origin]'
)
@click.option(
    '--new-remote', '-n',
    'new_remote',
    nargs=2,
    metavar='NAME URL',
    help='Remote server to install and use.'
)
@git_options
@ansible_output_options
def remote(repository, sync_destination, remote, new_remote, tag, refspec, branch, commit):
    """
    Synchronize a repository on a remote host at the
    sync_destination from the specified remote to the
    desired state.

    :param repository: name of the repository to sync
    :param sync_destination: repository location override
    :param remote: name of a remote server to sync from
    :param new_remote: name and url of a new remote server to add and sync from
    :param tag: tag to synchronize to
    :param refspec: refspec to synchronize to
    :param branch: branch to synchronize to (or create for refspec)
    :param commit: commit to synchronize to
    """
    validate_git_specifier(refspec, branch, commit, tag)
    validate_repository(repository)
    validate_remote(remote, new_remote)

    # We don't want to use default flag values as we cannot
    # tell if they are applied or not, and that makes validation
    # very difficult as we cannot determine what the user input.
    # Therefore, we can apply defaults now that we have validated.
    if not (refspec or branch or commit or tag):
        branch = 'master'

    if not (remote or new_remote):
        remote = 'origin'

    playbook_variables = dict(
        origin_ci_sync_repository=repository
    )

    if sync_destination:
        playbook_variables['origin_ci_sync_destination'] = sync_destination

    version_specifier = git_version_specifier(refspec, branch, commit, tag)
    for key in version_specifier:
        playbook_variables[key] = version_specifier[key]

    if new_remote:
        playbook_variables['origin_ci_sync_remote'] = new_remote[0]
        playbook_variables['origin_ci_sync_address'] = new_remote[1]
    else:
        playbook_variables['origin_ci_sync_remote'] = remote

    PlaybookRunner().run(
        playbook_source=playbook_path('sync/remote'),
        playbook_variables=playbook_variables
    )


def validate_repository(repository):
    """
    Validate that the repository can be synchronized
    using remote servers. Private repositories that
    exist on servers that require authentication cannot
    be synchronized from their remotes and must be updated
    using a local push instead.

    :param repository: repository to validate
    """
    if repository == Repository.enterprise:
        raise click.UsageError('Synchronizing the %s repository using remote servers is not supported.' % repository)


def validate_remote(remote, new_remote):
    """
    Validate that a remote was chosen.

    :param remote: name of an existing remote
    :param new_remote: name and url for a new remote
    """
    if new_remote and remote:
        raise click.UsageError('A new remote and existing remote cannot be specified at once.')
