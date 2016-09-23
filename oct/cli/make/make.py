# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import UsageError, command

from ..util.common_options import ansible_output_options
from ..util.make_options import make_options
from ..util.repository_options import repository_argument
from ...util.playbook import playbook_path
from ...util.playbook_runner import PlaybookRunner

_short_help = "Run targets from a repository's Makefile on the target host."


@command(
    short_help=_short_help,
    help=_short_help + '''

It may be necessary to have a more fine-grained interaction with
source repositories on remote hosts than what is possible with the
`build', `install', or `test' sub-commands of this tool. By choosing
a repository, make target and optionally some parameters, this command
allows for more specific control over actions on the remote host.

\b
Examples:
  Run only some Origin unit tests
  $ oct make origin test-unit --env WHAT=tools/junitreport/...
'''
)
@repository_argument
@make_options
@ansible_output_options
def make(repository, target, parameters, make_destination):
    """
    Execute some make targets on the remote host.

    :param repository: name of the repository in which to work
    :param target: make target or targets
    """
    playbook_variables = {
        'origin_ci_make_repository': repository,
        'origin_ci_make_targets': list(target)
    }

    if parameters:
        make_parameters = {}
        for param in parameters:
            if '=' not in param:
                raise UsageError('Parameter values must be a key-value pair. Parameter %s is invalid.' % param)
            (key, val) = param.split('=', 1)
            make_parameters[key] = val

        playbook_variables['origin_ci_make_parameters'] = make_parameters

    if make_destination:
        playbook_variables['origin_ci_make_destination'] = make_destination

    PlaybookRunner().run(
        playbook_source=playbook_path('make/main'),
        playbook_variables=playbook_variables
    )
