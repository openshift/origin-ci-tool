# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Choice, command, echo, option, pass_context

from .common_options import next_stage, package_options
from ..util.common_options import ansible_output_options

_short_help = 'Package a running Vagrant virtual machine.'


@command(
    short_help=_short_help,
    help=_short_help + '''

This command allows for a local virtual machine to be packaged
as an update for its current stage or as an instance of the next
stage in the pipeline.

For local development, it is possible to instruct this command to
update the Vagrant box metadata to point to a local file instead
of a URL for the backing VM image. Then, a `vagrant box add` can
be used to add the resulting metadata file to Vagrant as a box.

\b
Examples:
  Package a VM as a stage upgrade, bumping the minor version
  $ oct package vagrant --upgrade --bump-version=minor
\b
  Package a VM and let local files support the box
  $ oct package vagrant --serve-local --bump-version=none
''',
)
@ansible_output_options
@package_options
@option(
    '--bump-version',
    '-b',
    'bump_version',
    type=Choice([
        'major',
        'minor',
        'patch',
        'none',
    ]),
    required=True,
    help='Which version segment to bump.',
)
@option(
    '--serve-local/--serve-remote',
    '-l/-r',
    'serve_local_file',
    default=False,
    help='Point metadata reference to local file.  [default: remote]',
)
@pass_context
def vagrant(context, update_current_stage, serve_local_file, bump_version):
    """
    Package a running Vagrant virtual machine.

    :param context: Click context
    :param update_current_stage: whether or not to update current stage
    :param serve_local_file: whether or not to refer to the image locally in metadata
    :param bump_version: how to bump the box version
    """
    configuration = context.obj

    if bump_version == 'none':
        echo('Warning: not updating the version of the Vagrant box will mean users will not get these upgrades automatically.')

    for vm in configuration.registered_vagrant_machines():
        current_stage = vm.stage
        if update_current_stage:
            stage = current_stage
        else:
            stage = next_stage(current_stage)

        configuration.run_playbook(
            playbook_relative_path='package/vagrant',
            playbook_variables={
                'origin_ci_vagrant_target_stage': stage,
                'origin_ci_vagrant_hostname': vm.hostname,
                'origin_ci_vagrant_package_dir': configuration.vagrant_box_directory,
                'origin_ci_vagrant_package_ref': 'local' if serve_local_file else 'remote',  # TODO: just pass bool?
                'origin_ci_vagrant_package_bump_version': bump_version,
            },
        )

        # now that this VM has been used to package an image
        # for the `stage` stage, we should re-label it to be
        # an instance of that stage as well
        vm.stage = stage
        vm.write()
