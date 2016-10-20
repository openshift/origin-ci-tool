# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import ClickException, command, option, pass_context

from ..util.common_options import ansible_output_options
from ..util.repository_options import Repository, repository_argument

_short_help = 'Build binaries and other artifacts from source code.'


@command(
    short_help=_short_help,
    help=_short_help + '''

Once the source code in the repository on the remote host
is up-to-date or reflects the current state of the source
on the local development machine, it is necessary to build
the binaries and other artifacts from the source to allow
for an installation later in time. This command exposes a
single build flow for each repository.

\b
Examples:
  Build the binaries, images and RPMs for OpenShift Origin
  $ oct build origin
\b
  Build OpenShift Origin and everything that depends on it
  $ oct build origin --follow-dependencies
'''
)
@repository_argument
@option(
    '--follow-dependencies', '-f',
    'follow_dependencies',
    is_flag=True,
    default=False,
    show_default=True,
    help='Rebuild all child dependencies.'
)
@ansible_output_options
@pass_context
def build(context, repository, follow_dependencies):
    """
    Build the binaries and other artifacts necessary for
    the given repository on the remote host.

    :param context: Click context
    :param repository: name of the repository to use
    :param follow_dependencies: whether to rebuild all child dependencies or not
    """
    ansible_client = context.obj
    if repository == Repository.origin:
        build_origin(ansible_client, follow_dependencies)
    elif repository == Repository.enterprise:
        build_enterprise(ansible_client,follow_dependencies)
    elif repository == Repository.logging:
        build_logging(ansible_client)
    elif repository == Repository.metrics:
        build_metrics(ansible_client)
    elif repository == Repository.source_to_image:
        build_source_to_image(ansible_client)
    elif repository == Repository.web_console:
        build_web_console(ansible_client, follow_dependencies)


def build_origin(client, follow_dependencies):
    run_make(client, Repository.origin, 'rpm-release')
    if follow_dependencies:
        build_source_to_image(client)
        build_metrics(client)
        build_logging(client)


def build_enterprise(client, follow_dependencies):
    run_make(client, Repository.enterprise, 'rpm-release')
    if follow_dependencies:
        build_source_to_image(client)
        build_metrics(client)
        build_logging(client)


def build_logging(client):
    pass


def build_metrics(client):
    pass


def build_source_to_image(client):
    pass


def build_web_console(client, follow_dependencies):
    run_make(client, Repository.web_console, 'build')
    if follow_dependencies:
        run_make(client, Repository.origin, 'vendor-console')
        build_origin(client, follow_dependencies)

def run_make(client, repostory, target):
    client.run_playbook(
        playbook_relative_path='make/main',
        playbook_variables={
            'origin_ci_make_repository': repostory,
            'origin_ci_make_targets': [target]
        }
    )