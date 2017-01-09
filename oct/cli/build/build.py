# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import command, option, pass_context

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
''',
)
@repository_argument
@option(
    '--follow-dependencies', '-f',
    'follow_dependencies',
    is_flag=True,
    default=False,
    show_default=True,
    help='Rebuild all child dependencies.',
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
        build_enterprise(ansible_client, follow_dependencies)
    elif repository == Repository.logging:
        build_logging(ansible_client)
    elif repository == Repository.metrics:
        build_metrics(ansible_client)
    elif repository == Repository.source_to_image:
        build_source_to_image(ansible_client)
    elif repository == Repository.web_console:
        build_web_console(ansible_client, follow_dependencies)


def build_origin(ansible_client, follow_dependencies):
    build_openshift(ansible_client, Repository.origin, follow_dependencies)


def build_enterprise(ansible_client, follow_dependencies):
    build_openshift(ansible_client, Repository.enterprise, follow_dependencies)


def build_openshift(ansible_client, repository, follow_dependencies):
    run_make(ansible_client, repository, 'release-rpms')
    ansible_client.run_playbook(
        playbook_relative_path='prepare/local_rpm_repository',
        playbook_variables={
            'origin_ci_host_repository': repository,
        },
    )
    if follow_dependencies:
        build_source_to_image(ansible_client)
        build_metrics(ansible_client)
        build_logging(ansible_client)


def build_logging(ansible_client):
    run_make(ansible_client, Repository.logging, 'build-images')


def build_metrics(ansible_client):
    run_make(ansible_client, Repository.metrics, 'build-images')


def build_source_to_image(ansible_client):
    run_make(ansible_client, Repository.source_to_image, 'release')


def build_web_console(ansible_client, follow_dependencies):
    run_make(ansible_client, Repository.web_console, 'build')
    if follow_dependencies:
        run_make(ansible_client, Repository.origin, 'vendor-console')
        build_origin(ansible_client, follow_dependencies)


def run_make(ansible_client, repository, target):
    ansible_client.run_playbook(
        playbook_relative_path='make/main',
        playbook_variables={
            'origin_ci_make_repository': repository,
            'origin_ci_make_targets': [target],
        },
    )
