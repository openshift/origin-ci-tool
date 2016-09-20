import click

git_options_helptext = '''
\b
A git state is specified in one of the following ways:
 - a commit SHA in the current tree
 - a branch present locally or on a remote
 - a tag present locally or on a remote
 - a refspec and branch, where the refspec will
   be fetched and labeled with the branch name
'''


def git_options(func):
    """
    Add all of the Git ref options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    options = [
        git_refspec_option,
        git_branch_option,
        git_commit_option,
        git_tag_option
    ]

    for option in reversed(options):
        func = option(func)

    return func


def git_refspec_option(func):
    """
    Add the Git refspec option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--refspec', '-r',
        metavar='REF',
        help='Git ref spec to checkout.'
    )(func)


def git_branch_option(func):
    """
    Add the Git branch option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--branch', '-b',
        metavar='BRANCH',
        help='Git branch to checkout.  [default: master]'
    )(func)


def git_commit_option(func):
    """
    Add the Git commit option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--commit', '-c',
        metavar='SHA',
        help='Git commit SHA to checkout.'
    )(func)


def git_tag_option(func):
    """
    Add the Git tag option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--tag', '-t',
        metavar='TAG',
        help='Git tag to checkout.'
    )(func)


def validate_git_specifier(refspec, branch, commit, tag):
    """
    Validate that the set of specifiers given is consistent.
    The set is valid if:
     - only a branch is given
     - only a commit is given
     - only a tag is given
     - a refspec and target non-master branch is given

    :param refspec: provided refspec like 'pull/1/head'
    :param branch: provided branch like 'master'
    :param commit: provided commit SHA like '2cbd73cbd5aacc965ecfa480fa90164a85191489'
    :param tag: provided tag like 'v1.3.0-rc2'
    """
    if commit and (refspec or branch or tag):
        raise click.UsageError('If a commit is specified, neither a refspec, branch, or tag can also be specified.')

    if tag and (commit or refspec or branch):
        raise click.UsageError('If a tag is specified, neither a refspec, branch, or commit can also be specified.')

    if branch and (commit or tag):
        raise click.UsageError('If a branch is specified, neither a tag or commit can also be specified.')

    if refspec and (commit or tag):
        raise click.UsageError('If a refspec is specified, neither a tag or commit can also be specified.')

    if refspec and not branch:
        raise click.UsageError('If a refspec is specified, the name of the branch to create for it is required.')

    if refspec and branch and branch == 'master':
        raise click.UsageError('If a branch is specified for a refspec, it cannot be the master branch.')


def git_version_specifier(refspec, branch, commit, tag):
    """
    Return the minimal set of specifiers that the user
    input reduces to, in a dict of variables for Ansible.

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

    if branch and not refspec:
        return {'origin_ci_sync_version': branch}

    if branch and refspec:
        return {
            'origin_ci_sync_version': branch,
            'origin_ci_sync_refspec': refspec + ':' + branch
        }
