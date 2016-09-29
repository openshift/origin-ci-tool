# coding=utf-8
from __future__ import absolute_import, division, print_function

from StringIO import StringIO
from copy import deepcopy
from shutil import rmtree
from subprocess import check_output

from os.path import join
from paramiko import SSHConfig
from yaml import dump, load

_variable_name_to_metadata_field = {
    'origin_ci_vagrant_home_dir': 'directory',
    'origin_ci_vagrant_os': 'operating_system',
    'origin_ci_vagrant_provider': 'provider',
    'origin_ci_vagrant_stage': 'stage',
    'origin_ci_vagrant_hostname': 'hostname',
    'ansible_ssh_host': 'host',
    'ansible_ssh_port': 'port',
    'ansible_ssh_private_key_file': 'private_key_file',
    'ansible_ssh_user': 'remote_user',
    'ansible_ssh_extra_args': 'extra_ssh_args'
}


def fetch_ssh_configuration(hostname, directory):
    """
    Fetch the SSH configuration options that Vagrant
    holds for the VM with the specified hostname in
    the local directory.

    :param hostname: name of the Vagrant VM
    :param directory: "location" of the Vagrant VM
    :return: SSH configuration
    """
    config = SSHConfig()
    config.parse(StringIO(unicode(check_output(['vagrant', 'ssh-config', '--host', hostname], cwd=directory))))
    return config.lookup(hostname)


class VagrantVMMetadata(object):
    """
    This container holds the relevant metadata
    for Vagrant VM guests we have provisioned.
    """

    def __init__(self, data=None, variable_file=None):
        self.directory = None
        self.operating_system, self.provider, self.stage = None, None, None
        self.hostname, self.host, self.port = None, None, None
        self.private_key_file, self.remote_user, self.extra_ssh_args = None, None, None
        self.extra = {}

        # Either raise a custom exception or use a better built in exception
        # https://docs.python.org/2/library/exceptions.html#exception-hierarchy

        # this is an overloaded constructor since we will
        # want to create metadata objects in one of two
        # distinct ways: either from the constituent data
        # or from a file containing variables on disk
        if data is not None and variable_file is not None:
            raise Exception('Vagrant VM Metadata should be initialized with a file or with data, not both!')
        elif data is not None:  # Is it possible to have key errors here?
            self.set_metadata(data['directory'], data['hostname'], data['provisioning_details'])
        elif variable_file is not None: # this is probably what you meant
        # elif file:  # dynamic languages have the greatest bugs :)
            self.load(variable_file)
        else:
            raise Exception('Vagrant VM Metadata should be initialized with a file or with data, not neither!')

    def set_metadata(self, directory, hostname, provisioning_details):
        """
        Initialize the VM metadata using explicit data.

        :param directory: directory where the VM was created
        :param hostname: hostname for the VM guest
        :param provisioning_details: options used to provision the VM
        """
        # "location" of the Vagrant VM on the local host
        self.directory = directory

        # provisioning details
        self.operating_system = provisioning_details['operating_system']
        self.provider = provisioning_details['provider']
        self.stage = provisioning_details['stage']

        # SSH connection details
        self.hostname = hostname

        ssh_configuration = fetch_ssh_configuration(hostname, directory)
        self.host = ssh_configuration['hostname']
        self.port = ssh_configuration['port']
        self.private_key_file = ','.join(ssh_configuration['identityfile'])
        self.remote_user = ssh_configuration['user']

        extra_ssh_flags = [
            'userknownhostsfile',
            'stricthostkeychecking',
            'passwordauthentication',
            'identitiesonly',
            'loglevel'
        ]
        extra_args = []
        for flag in extra_ssh_flags:
            if flag in ssh_configuration:
                extra_args.append('-o {}={}'.format(flag, ssh_configuration[flag]))
        self.extra_ssh_args = ' '.join(extra_args)

    def load(self, variable_file):
        """
        Initialize the VM metadata using a variables file.

        :param variable_file: path to local file with VM data
        """
        with open(variable_file) as variables:
            raw_data = load(variables)
            # data in the variable file we don't understand
            self.extra = {k: v for k, v in raw_data.iteritems() if k not in _variable_name_to_metadata_field}

            for variable, field in _variable_name_to_metadata_field.iteritems():
                setattr(self, field, raw_data[variable])

    def write(self):
        """
        Serialize VM metadata to disk.
        """
        raw_data = deepcopy(self.extra)
        for variable, field in _variable_name_to_metadata_field.iteritems():
            raw_data[variable] = getattr(self, field)

        # not sure why you would need w+, wb is best practice for windows compatibility
        with open(join(self.directory, 'variables.yml'), 'wb') as variables_file:
            dump(raw_data, variables_file, default_flow_style=False, explicit_start=True)

    def remove(self):
        """
        Remove Vagrant VM metadata from disk.
        """
        rmtree(self.directory)
