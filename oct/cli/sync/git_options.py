# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import UsageError, option

git_options_helptext = '''
\b
A git state is specified in one of the following ways:
 - a commit SHA in the current tree
 - a branch present locally or on a remote
 - a tag present locally or on a remote
 - a refspec and branch, where the refspec will
   be fetched and labeled with the branch name
 - (optionally) a second branch reference into
   which the state specified above will be merged
   into on the remote host
'''


def git_options(func):
    """
    Add all of the Git ref options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    click_options = [
        git_refspec_option,
        git_branch_option,
        git_commit_option,
        git_tag_option,
        git_destination_option,
    ]

    for click_option in reversed(click_options):
        func = click_option(func)

    return func


def git_refspec_option(func):
    """
    Add the Git refspec option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--refspec',
        '-r',
        metavar='REF',
        help='Git ref spec to checkout.',
    )(func)


def git_branch_option(func):
    """
    Add the Git branch option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--branch',
        '-b',
        metavar='BRANCH',
        help='Git branch to checkout.  [default: master]',
    )(func)


def git_commit_option(func):
    """
    Add the Git commit option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--commit',
        '-c',
        metavar='SHA',
        help='Git commit SHA to checkout.',
    )(func)


def git_tag_option(func):
    """
    Add the Git tag option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--tag',
        '-t',
        metavar='TAG',
        help='Git tag to checkout.',
    )(func)


def git_destination_option(func):
    """
    Add the Git destination option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--merge-into',
        '-m',
        'merge_target',
        metavar='BRANCH',
        help='Git branch to merge synced state into.',
    )(func)


def validate_git_specifier(pullrefs, refspec, branch, commit, tag):
    """
    Validate that the set of specifiers given is consistent.
    The set is valid if:
     - only a branch is given
     - only a commit is given
     - only a tag is given
     - a refspec and target non-master branch is given
     - a pullrefs and target non-master branch is given

    :param pullrefs: pull request references inside prow like 'master:97d901d8e7,4:bcb00a13b2'
    :param refspec: provided refspec like 'pull/1/head'
    :param branch: provided branch like 'master'
    :param commit: provided commit SHA like '2cbd73cbd5aacc965ecfa480fa90164a85191489'
    :param tag: provided tag like 'v1.3.0-rc2'
    """
    if commit and (pullrefs or refspec or branch or tag):
        raise UsageError('If a commit is specified, neither a pullrefs, refspec, branch, or tag can also be specified.')

    if tag and (commit or refspec or pullrefs or branch):
        raise UsageError('If a tag is specified, neither a pullrefs, refspec, branch, or commit can also be specified.')

    if refspec and not branch:
        raise UsageError('If a refspec is specified, the name of the branch to create for it is required.')

    if pullrefs and not branch:
        raise UsageError('If a pullrefs is specified, the name of the branch to create for it is required.')

    if refspec and branch == 'master':
        raise UsageError('The branch specified for a refspec cannot be the master branch.')

    if pullrefs and branch == 'master':
        raise UsageError('The branch specified for a pullrefs cannot be the master branch.')


def git_version_specifier(pullrefs, refspec, branch, commit, tag):
    """
    Return the minimal set of specifiers that the user
    input reduces to, in a dict of variables for Ansible.

    :param pullrefs: pull request references inside prow like 'master:97d901d8e7,4:bcb00a13b2'
    :param refspec: provided refspec like 'pull/1/head'
    :param branch: provided branch like 'master'
    :param commit: provided commit SHA like '2cbd73cbd5aacc965ecfa480fa90164a85191489'
    :param tag: provided tag like 'v1.3.0-rc2'
    :return: minimal set of specifiers in a dict using Ansible keys
    """
    if commit:
        return {'origin_ci_sync_version': commit}

    if tag:
        return {'origin_ci_sync_version': tag}

    if branch and pullrefs:
        pull_refs = []
        for pull_num in [r.split(':')[0] for r in pullrefs.split(',')][1:]:
            pull_refs.append(pull_num)
        return {
            'origin_ci_sync_version': branch,
            'origin_ci_pull_refs': pull_refs,
        }

    if branch and refspec:
        return {
            'origin_ci_sync_version': branch,
            'origin_ci_sync_refspec': refspec + ':' + branch,
        }

    if branch:
        return {'origin_ci_sync_version': branch}
