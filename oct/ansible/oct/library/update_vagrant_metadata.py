# coding=utf-8
"""
update_vagrant_metadata is an Ansible module that allows for
updates to a single provider section of a Vagrant metadata.json
file describing a box.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from json import dump, load

from ansible.module_utils.basic import AnsibleModule
from semver import bump_major, bump_minor, bump_patch

DOCUMENTATION = '''
---
module: update_vagrant_metadata
short_description: Update Vagrant metadata.json Files
author: Steve Kuznetsov
options:
  dest:
    description:
      - The location of the metadata.json file to change.
    required: true
  version_increment:
    description:
      - Which part of the box version to update.
    required: true
    choices: [ 'major', 'minor', 'patch', 'none' ]
  provider:
    description:
      - The Vagrant provider for which to change data.
    required: true
    choices: [ 'libvirt', 'virtualbox', 'vmware_fusion' ]
  checksum:
    description:
      - The value of the new image checksum.
    required: true
  serve_local:
    description:
      - From where to serve the box on the local host.
    required: false
requirements:
 - semver
'''

EXAMPLES = '''
# Update the libvirt checksum for the latest version in a metadata file
- update_vagrant_metadata:
    dest: '/home/origin/.config/origin-ci-tool/vagrant/boxes/fedora/base/metadata.json'
    version_increment: 'patch'
    provider: 'libvirt'
    checksum: '3e1fc0abbf772899adc95a3dda776120'

# Update the libvirt checksum for the latest version in a metadata file and serve the image locally
- update_vagrant_metadata:
    dest: '/home/origin/.config/origin-ci-tool/vagrant/boxes/fedora/base/metadata.json'
    version_increment: 'patch'
    provider: 'libvirt'
    checksum: '3e1fc0abbf772899adc95a3dda776120'
    serve_local: '/home/origin/.config/origin-ci-tool/vagrant/boxes/fedora/base/fedora_base.qcow2'
# '''


def main():
    """
    Update a Vagrant metadata.json file to bump the box version
    and record a new image checksum, optionally choosing to serve
    the new image from the local host.
    """
    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=dict(
            dest=dict(
                required=True,
                default=None,
                type='str'
            ),
            version_increment=dict(
                required=False,
                default=None,
                type='str',
                choices=[
                    'major',
                    'minor',
                    'patch'
                ]
            ),
            provider=dict(
                required=True,
                default=None,
                type='str',
                choices=[
                    'libvirt',
                    'virtualbox',
                    'vmware_fusion'
                ]
            ),
            checksum=dict(
                required=True,
                default=None,
                type='str'
            ),
            serve_local=dict(
                required=False,
                default=None,
                type='str'
            )
        )
    )

    metadata_path = module.params['dest']
    version_increment = module.params['version_increment']
    provider = module.params['provider']
    checksum = module.params['checksum']
    serve_local = module.params['serve_local']

    with open(metadata_path) as metadata_file:
        current_metadata = load(metadata_file)

    new_version = update_metadata(current_metadata['versions'][0], version_increment, provider, checksum, serve_local)
    del current_metadata['versions']
    current_metadata['versions'] = [new_version]

    with open(metadata_path, 'wb') as metadata_file:
        dump(current_metadata, metadata_file, indent=2)

    module.exit_json(
        changed=True,
        failed=False,
        dest=metadata_path,
        version_increment=version_increment,
        provider=provider,
        checksum=checksum,
        serve_local=serve_local
    )


def update_metadata(metadata, version_increment, provider, checksum, serve_local):
    if version_increment == 'major':
        metadata['version'] = bump_major(metadata['version'])
    elif version_increment == 'minor':
        metadata['version'] = bump_minor(metadata['version'])
    elif version_increment == 'patch':
        metadata['version'] = bump_patch(metadata['version'])

    current_provider_data = None
    for provider_data in metadata['providers']:
        if provider_data['name'] == provider:
            current_provider_data = provider_data
            break

    current_provider_data['checksum'] = checksum
    if serve_local:
        current_provider_data['url'] = serve_local

    return metadata


if __name__ == '__main__':
    main()
