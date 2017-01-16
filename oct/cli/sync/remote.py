# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import UsageError, command, option, pass_context

from .git_options import git_options, git_options_helptext, git_version_specifier, validate_git_specifier
from .sync_options import sync_destination_option
from ..util.common_options import ansible_output_options
from ..util.repository_options import Repository, repository_argument

_SHORT_HELP = 'Synchronize a repository using remote servers.'


@command(
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

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
  Synchronize the Origin repo, specifying a branch on an existing remote
  $ oct sync remote origin --remote=myfork --branch=my-feature-branch
\b
  Synchronize the logging repo, specifying a specific branch
  $ oct sync remote origin-aggregated-logging --branch=enterprise
\b
  Synchronize the Origin repo, specifying a pull request refspec
  $ oct sync remote origin --refspec=pull/1000/head --branch=pull-1000
\b
  Synchronize the Origin repo, resulting in a merged state of two branches
  $ oct sync remote origin --remote=myfork --branch=my-feature-branch --merge-into=master
''',
)
@repository_argument
@sync_destination_option
@option(
    '--remote',
    '-r',
    'remote_name',
    metavar='NAME',
    help='Named remote server to use.  [default: origin]',
)
@option(
    '--new-remote',
    '-n',
    'new_remote',
    nargs=2,
    metavar='NAME URL',
    help='Remote server to install and use.',
)
@git_options
@ansible_output_options
@pass_context
def remote(context, repository, sync_destination, remote_name, new_remote, tag, refspec, branch, commit, merge_target):
    """
    Synchronize a repository on a remote host at the
    sync_destination from the specified remote to the
    desired state.

    :param context: Click context
    :param repository: name of the repository to sync
    :param sync_destination: repository location override
    :param remote_name: name of a remote server to sync from
    :param new_remote: name and url of a new remote server to add and sync from
    :param tag: tag to synchronize to
    :param refspec: refspec to synchronize to
    :param branch: branch to synchronize to (or create for refspec)
    :param commit: commit to synchronize to
    :param merge_target: optional second branch to merge the state into
    """
    validate_git_specifier(refspec, branch, commit, tag)
    validate_repository(repository)
    validate_remote(remote_name, new_remote)

    # We don't want to use default flag values as we cannot
    # tell if they are applied or not, and that makes validation
    # very difficult as we cannot determine what the user input.
    # Therefore, we can apply defaults now that we have validated.
    if not (refspec or branch or commit or tag):
        branch = 'master'

    if not (remote_name or new_remote):
        remote_name = 'origin'

    playbook_variables = {'origin_ci_sync_repository': repository, }

    if sync_destination:
        playbook_variables['origin_ci_sync_destination'] = sync_destination

    if merge_target:
        playbook_variables['origin_ci_sync_merge_target'] = merge_target

    version_specifier = git_version_specifier(refspec, branch, commit, tag)
    for key in version_specifier:
        playbook_variables[key] = version_specifier[key]

    if new_remote:
        playbook_variables['origin_ci_sync_remote'] = new_remote[0]
        playbook_variables['origin_ci_sync_address'] = new_remote[1]
    else:
        playbook_variables['origin_ci_sync_remote'] = remote_name

    context.obj.run_playbook(
        playbook_relative_path='sync/remote',
        playbook_variables=playbook_variables,
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
        raise UsageError('Synchronizing the %s repository using remote servers is not supported.' % repository)


def validate_remote(existing_remote, new_remote):
    """
    Validate that a remote was chosen.

    :param existing_remote: name of an existing remote
    :param new_remote: name and url for a new remote
    """
    if new_remote and existing_remote:
        raise UsageError('A new remote and existing remote cannot be specified at once.')
