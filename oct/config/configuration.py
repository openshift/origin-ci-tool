# coding=utf-8
from __future__ import absolute_import, division, print_function

from itertools import chain

from os import getenv, listdir, mkdir
from os.path import abspath, exists, expanduser, isdir, join
from yaml import dump, load

from ..config.ansible_client import AnsibleCoreClient
from ..config.vagrant import VagrantVMMetadata
from ..config.variables import PlaybookExtraVariables
from ..util.playbook import playbook_path

DEFAULT_HOSTNAME = 'openshiftdevel'

_ANSIBLE_CONFIGURATION_FILE = 'ansible_configuration.yml'
_ANSIBLE_VARIABLES_FILE = 'ansible_variables.yml'


# Stop using the word yeild
# Yield != return

class Configuration(object):
    """
    This container holds all of the state that this tool needs
    to persist between CLI invocations. Default values allow
    for playbooks to be run with a minimal amount of specification.
    `run_playbook()` acts as a minimal client for the Ansible API.
    """

    def __init__(self):
        # Configuration will be placed in the user-based conf-
        # iguration path as per the XDG basedir specification:
        # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
        base_dir = getenv('XDG_CONFIG_HOME', expanduser('~'))

        # path to the local configuration directory
        self._path = abspath(join(base_dir, '.config', 'origin-ci-tool'))

        if not exists(self._path):
            mkdir(self._path)

        # This may be easier to read if instead of setting these vars throughout functions
        # you just have them return the value and assign it here

        # configuration options for Ansible core
        self.ansible_configuration = None
        self.load_ansible_configuration()

        # extra variables we want to send to Ansible playbooks
        self.ansible_variables = None
        self.load_ansible_variables()

        # metadata about active Vagrant local VMs
        self._vagrant_metadata = []
        self.load_vagrant_metadata()

    def run_playbook(self, playbook_relative_path, playbook_variables=None):
        """
        Run a playbook from file with the variables provided. The
        playbook file should be specified as a relative path from
        the root of the internal Ansible playbook directory, with
        the YAML suffix omitted, e.g. `prepare/main`

        :param playbook_relative_path: the location of the playbook
        :param playbook_variables: extra variables for the playbook
        """
        self.ansible_configuration.run_playbook(
            playbook_file=playbook_path(playbook_relative_path),
            playbook_variables=self.ansible_variables.default(playbook_variables)
        )

    @property
    def configuration_path(self):
        """
        Return the path to the Ansible core configuration file.
        :return: absolute path to the Ansible core configuration
        """
        return join(self._path, _ANSIBLE_CONFIGURATION_FILE)

    def load_ansible_configuration(self):
        """
        Load the Ansible core configuration options from disk,
        or if they have not yet been written to disk, use the
        default values and write them for future callers.
        """
        if not exists(self.configuration_path):
            self.ansible_configuration = AnsibleCoreClient()
            self.write_ansible_configuration()
        else:
            with open(self.configuration_path) as configuration_file:
                self.ansible_configuration = load(configuration_file)

    def write_ansible_configuration(self):
        """
        Write the current set of Ansible core configuration
        options to disk.
        """
        with open(self.configuration_path, 'w+') as configuration_file:
            dump(
                self.ansible_configuration,
                configuration_file,
                default_flow_style=False,
                explicit_start=True
            )

    @property
    def variables_path(self):
        """
        Yield the path to the Ansible playbook extra variables file.
        :return: absolute path to the Ansible playbook extra variables
        """
        return join(self._path, _ANSIBLE_VARIABLES_FILE)

    def load_ansible_variables(self):
        """
        Load the Ansible extra playbook variables from disk,
        or if they have not yet been written to disk, use the
        default values and write them for future callers.
        """
        if not exists(self.variables_path):
            self.ansible_variables = PlaybookExtraVariables()
            self.write_ansible_variables()
        else:
            with open(self.variables_path) as variables_file:
                self.ansible_variables = load(variables_file)

    def write_ansible_variables(self):
        """
        Write the current set of Ansible extra playbook
        variables to disk.
        """
        with open(self.variables_path, 'w+') as variables_file:
            dump(
                self.ansible_variables,
                variables_file,
                default_flow_style=False,
                explicit_start=True
            )

    def write_configuration(self):
        """
        Write the entire set of configuration options to disk.
        """
        self.write_ansible_configuration()
        self.write_ansible_variables()

    @property
    def vagrant_directory_root(self):
        """
        Return the root path for Vagrant VM locations.
        :return: absolute path to Vagrant VM containers directory
        """
        return join(self._path, 'vagrant')

    def vagrant_home_directory(self, name):
        """
        Yield the path to the specific storage directory
        for the VM `boxname'.

        :param name: name of the VM
        :return: absolute path to the Vagrant VM directory
        """
        return join(self.vagrant_directory_root, name)

    @property
    def next_available_vagrant_name(self):
        """
        Yield the next available hostname for a local Vagrant
        VM.

        :return: the next hostname
        """
        if not self._vagrant_hostname_taken(DEFAULT_HOSTNAME):
            return DEFAULT_HOSTNAME

        for i in range(len(listdir(self.vagrant_directory_root)) + 1):
            possible_hostname = DEFAULT_HOSTNAME + str(i)
            if not self._vagrant_hostname_taken(possible_hostname):
                return possible_hostname

    def _vagrant_hostname_taken(self, name):
        """
        Determine if a Vagrant VM with the given hostname exists.

        :param name: hostname of the VM
        :return: whether or not the VM exists
        """
        # we know all of our Vagrant VMs must reside in top-
        # level subdirectories of the Vagrant directory root,
        # so we can do this simple exists check
        return isdir(join(self.vagrant_directory_root, name))

    def load_vagrant_metadata(self):
        """
        Load metadata for the Vagrant virtual machines
        that we have provisioned with this tool.
        """
        if not exists(self.vagrant_directory_root):
            mkdir(self.vagrant_directory_root)
        else:
            for content in listdir(self.vagrant_directory_root):
                variables_file = join(self.vagrant_directory_root, content, 'variables.yml')
                if exists(variables_file):
                    self.register_vagrant_host(VagrantVMMetadata(variable_file=variables_file))

    def registered_vagrant_machines(self):
        """
        Yield the list of Vagrant machine metadata.
        :return: the Vagrant metadata
        """
        return self._vagrant_metadata

    def register_vagrant_host(self, data):
        """
        Register a new host by updating metadata records for the
        new VM both in the in-memory cache for this process and
        the on-disk records that will persist past this CLI call.

        :param data: VagrantVMMetadata for the host
        """
        if not isinstance(data, VagrantVMMetadata):  # Why is a type check needed?  It's not like you make sure of types anywhere else
            raise TypeError('Registering a machine requires {}, got {} instead!'.format(type(VagrantVMMetadata), type(data)))
        else:
            self._vagrant_metadata.append(data)
            data.write()

    def _get_config(self, key):
        if hasattr(self.ansible_configuration, key):
            return self.ansible_configuration
        elif hasattr(self.ansible_variables, key):
            return self.ansible_variables
        else:
            raise KeyError('No such option `{}`.'.format(key))

    def __getitem__(self, key):
        """
        Fetch the configuration key. Makes the inclusion
        of variables and options as separate fields in this
        meta-container transparent to users.

        :param key: name of the item to fetch
        :return: value of the item
        """
        return getattr(self._get_config(key), key)

    def __setitem__(self, key, value):
        """
        Update the value of the configuration entry. Makes
        the inclusion of variables and options as separate
        fields in this meta-container transparent to users.

        :param key: name of the item to update
        :param value: value to update the item to
        """
        setattr(self._get_config(key), key, value)

    def __contains__(self, key):
        """
        Determine if the underlying containers in fact
        contain the configuration item.

        :param key: name of the item to search for
        :return: whether or not we contain the item
        """
        return hasattr(self.ansible_configuration, key) or hasattr(self.ansible_variables, key)

    def __iter__(self):
        """
        Return an iterator for contained properties.

        :return: the iterator
        """
        return chain(vars(self.ansible_variables).iteritems(), vars(self.ansible_configuration).iteritems())
