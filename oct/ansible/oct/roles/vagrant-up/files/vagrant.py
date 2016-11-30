#!/usr/bin/env python
# coding=utf-8
"""
Vagrant external inventory script. Automatically
searches for Vagrant boxes under the configured
directory and returns that inventory with SSH
configuration and the contents of the hosts' var
file for each host.

Hosts will all be placed under the `vms' group
and additionally into any groups as labelled in
the host's group file, which should be a simple
YAML serialized list.

We expect to find Vagrant VMs under the Origin
CI Tool configuration directory, often stored at:
   ~/.config/origin-ci-tool/vagrant

In each subdirectory, we expect to find:
 - a single Vagrant VM started from the canonical
   Vagrantfile
 - optionally a `groups.yml' file specifying
   which Ansible inventory groups this host should
   be a member of
 - optionally a `variables.yml` file specifying
   which Ansible host variables should be set for
   this host
"""
from __future__ import absolute_import, division, print_function

from json import dumps
from optparse import OptionParser
from subprocess import check_output
from sys import exit

from os import getenv, listdir
from os.path import abspath, exists, expanduser, isdir, join
from re import search
from yaml import load

parser = OptionParser(usage='%prog --list | --host <machine>')
parser.add_option(
    '--list',
    default=False,
    dest='list',
    action='store_true',
    help='Emit a full inventory as a JSON mapping of groups to hostnames and variables.'
)
parser.add_option(
    '--host',
    default=None,
    dest='host',
    help='Emit host metadata for a specific host as a JSON mapping of key-value pairs.'
)
(options, args) = parser.parse_args()


def get_vagrant_info(vm_directory):
    """
    Determine if a running Vagrant VM exists at the
    specified directory, and, if so, determine the
    Ansible inventory groups it belongs to and any
    variables that are tied to this host.

    :param vm_directory: directory to issue `vagrant' commands in
    :return: (hostname, groups, variables)
    """
    hostname = determine_vagrant_hostname(vm_directory)
    if not hostname:
        # no running VM exists in this directory
        return None, None, None

    groups = determine_inventory_groups(vm_directory)
    variables = determine_host_variables(vm_directory)
    return hostname, groups, variables


def determine_vagrant_hostname(vm_directory):
    """
    Determine the name of the Vagrant VM in the
    specified directory. We control the Vagrantfile
    used to launch VMs in these directories, so we
    can be certain that there will only be one
    active VM in any one directory.

    :param vm_directory: directory to issue `vagrant' commands in
    :return: the name of the running VM, or None
    """
    for line in check_output(['vagrant', 'status'], cwd=vm_directory).splitlines():
        matches = search('([^\s]+)[\s]+running \(.+', line)
        if matches:
            return matches.group(1)


def determine_inventory_groups(vm_directory):
    """
    Determine the Ansible inventory groups that this
    VM is a member of.

    :param vm_directory: directory to issue `vagrant' commands in
    :return: list of Ansible inventory groups
    """
    group_config = join(vm_directory, 'groups.yml')
    if exists(group_config):
        with open(group_config) as group_file:
            return load(group_file)
    else:
        return []


def determine_host_variables(vm_directory):
    """
    Determine the Ansible host variables that this
    VM is decorated with by default.

    :param vm_directory: directory to issue `vagrant' commands in
    :return: dictionary of variables
    """
    vars_config = join(vm_directory, 'variables.yml')
    if exists(vars_config):
        with open(vars_config) as vars_file:
            return load(vars_file)
    else:
        return {}


def add_host_to_inventory(inventory, hostname, groups, variables):
    """
    Add the given host to the inventory container.

    :param inventory: partially-filled inventory
    :param hostname: hostname of the new host
    :param groups: groups the host belongs to
    :param variables: host variables for the new host
    """
    # all hosts are in the `vms' group
    inventory['vms']['hosts'].append(hostname)

    # additionally a host can be in other groups
    for group in groups:
        if group not in inventory:
            inventory[group] = {
                'hosts': [],
                'vars': {}
            }

        inventory[group]['hosts'].append(hostname)

    # we store the host-specific variables in `_meta'
    # to reduce the amount of disk traffic necessary
    # when fetching more information
    inventory['_meta']['hostvars'][hostname] = variables


def determine_base_path():
    """
    Determine the user-based configuration path as per
    the XDG basedir specification:
    https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

    :return: base path for the configuration dir
    """
    config_dir = getenv('XDG_CONFIG_HOME', expanduser('~'))
    return abspath(join(config_dir, '.config', 'origin-ci-tool', 'vagrant'))


def list_vagrant_directories():
    """
    List all possible Vagrant VM directories.

    :return: list of potential Vagrant VM directories
    """
    base_directory = determine_base_path()
    vagrant_directories = []
    for entry in listdir(base_directory):
        entry = join(base_directory, entry)
        if isdir(entry) and not entry.endswith('boxes'):
            vagrant_directories.append(entry)

    return vagrant_directories


if options.list:
    full_inventory = {
        '_meta': {
            'hostvars': {}
        },
        'vms': {
            'hosts': [],
            'vars': {}
        }
    }

    # load VM hosts
    for directory in list_vagrant_directories():
        current_hostname, host_groups, host_variables = get_vagrant_info(directory)
        if current_hostname:
            add_host_to_inventory(full_inventory, current_hostname, host_groups, host_variables)

    print(dumps(full_inventory))

elif options.host:
    # terribly inefficient implementation, only useful
    # if someone manages to make this run with an old
    # version of Ansible
    for directory in list_vagrant_directories():
        current_hostname, host_groups, host_variables = get_vagrant_info(directory)
        if current_hostname == options.host:
            print(dumps(host_variables))
            exit(0)

    print(dumps({}))

else:
    parser.print_help()
    exit(2)
