# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, pass_context

from .git_options import git_options, git_options_helptext, git_version_specifier, validate_git_specifier
from .sync_options import sync_options
from ..util.common_options import ansible_output_options
from ..util.repository_options import repository_argument

_SHORT_HELP = 'Synchronize a repository using local sources.'


@command(
    short_help=_SHORT_HELP,
    help=_SHORT_HELP + '''

The local Git client can be used to synchronize the repositories
on remote hosts with local copies by directly pushing to a ref
over SSH. This command will do so, creating automated commits
in order to preserve the state of staged and unstaged changes
in the working tree.

Both the sync source directory on the local host and the sync
destination directory on the remote hosts are optional if the
$GOPATH environment variable is set, as they will be assumed
to be of the following form, where '<REPOSITORY>' is the single
argument accepted by this command:
    $GOPATH/src/github.com/openshift/<REPOSITORY>

''' + git_options_helptext + '''

\b
Examples:
  Synchronize the Origin repo, auto-detecting locations
  $ oct sync local origin
\b
  Synchronize the S2I repo, specifying the local location
  $ oct sync local source-to-image --src="${HOME}/source-to-image"
\b
  Synchronize the Origin repo, specifying a local branch
  $ oct sync local origin --branch=my-feature-branch
\b
  Synchronize the Origin repo, resulting in a merged state of two branches
  $ oct sync local origin --branch=my-feature-branch --merge-into=master
''',
)
@repository_argument
@sync_options
@git_options
@ansible_output_options
@pass_context
def local(context, repository, sync_source, sync_destination, tag, refspec, branch, commit, merge_target):
    """
    Synchronize a repository on a remote host at the
    sync_destination by pushing the git state of the
    repository on the local machine at the sync_source.

    :param context: Click context
    :param repository: name of the repository to sync
    :param sync_source: local repository location override
    :param sync_destination: repository location override
    :param tag: tag to synchronize to
    :param refspec: refspec to synchronize to
    :param branch: branch to synchronize to (or create for refspec)
    :param commit: commit to synchronize to
    :param merge_target: optional second branch to merge the state into
    """
    validate_git_specifier(pullrefs=None, refspec=refspec, branch=branch, commit=commit, tag=tag)

    # We don't want to use default flag values as we cannot
    # tell if they are applied or not, and that makes validation
    # very difficult as we cannot determine what the user input.
    # Therefore, we can apply defaults now that we have validated.
    if not (refspec or branch or commit or tag):
        branch = 'master'

    playbook_variables = {'origin_ci_sync_repository': repository, }

    if sync_source:
        playbook_variables['origin_ci_sync_source'] = sync_source

    if sync_destination:
        playbook_variables['origin_ci_sync_destination'] = sync_destination

    if merge_target:
        playbook_variables['origin_ci_sync_merge_target'] = merge_target

    version_specifier = git_version_specifier(pullrefs=None, refspec=refspec, branch=branch, commit=commit, tag=tag)
    for key in version_specifier:
        playbook_variables[key] = version_specifier[key]

    context.obj.run_playbook(
        playbook_relative_path='sync/local',
        playbook_variables=playbook_variables,
    )
