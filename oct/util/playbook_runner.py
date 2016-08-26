from collections import namedtuple

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager


class PlaybookRunner:
    '''
    This class allows for a simple abstraction around the loading
    and execution of an Ansible playbook given an inventory and
    variables to expose to the playbook.
    '''

    def __init__(self,
                 variable_manager=VariableManager(), data_loader=DataLoader(), host_list=None, passwords=None,
                 connection='local', module_path='', forks=5, become=True, become_method='sudo', become_user='root', check=False
                 # TODO: probably shouldn't be defaulting to root and sudo, as proper setup will give us correct user
                 ):
        """
        Initialize a PlaybookRunner.

        :param variable_manager: instance of an Ansible variable manager
        :param data_loader: instance of an Ansible data loader
        :param host_list: either a literal list of hosts or the path to an inventory file
        :param passwords: passwords to use when connection to remote hosts
        :param connection: what type of connection to use to connect to the host, one of ssh, local, docker
        :param module_path: path to third-party modules to load
        :param forks: number of parallel processes to spawn when communicating with remote hosts
        :param become: determine if privilege escalation should be activated
        :param become_method: method to use for privilege escalation
        :param become_user: user to assume in order to escalate priviliges
        :param check: do a dry run, simulating actions Ansible would take on a remote host
        """
        self._variable_manager = variable_manager
        self._data_loader = data_loader

        ansible_playbook_options = namedtuple(
            'Options', [
                'connection',
                'module_path',
                'forks',
                'become',
                'become_method',
                'become_user',
                'check',
                # listing options, which we won't use here
                'listhosts',
                'listtasks',
                'listtags',
                'syntax'
            ]
        )

        self._ansible_playbook_options = ansible_playbook_options(
            connection=connection,
            module_path=module_path,
            forks=forks,
            become=become,
            become_method=become_method,
            become_user=become_user,
            check=check,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None
        )

        self._passwords = passwords
        self._inventory = Inventory(loader=data_loader, variable_manager=variable_manager, host_list=host_list)
        self._variable_manager.set_inventory(self._inventory)

    def run(self, playbook_source, vars=None):
        """
        Run a playbook defined in the file at playbook_source with the variables provided.

        :param playbook_source: the location of the playbook to run
        :param vars: a dictionary of variables to pass to the playbook
        """

        # TODO: remove this defaulting step once we have user config
        if not vars:
            vars = dict(
                origin_ci_hosts='localhost',
                origin_ci_connection='local'
            )

        # we don't really care which hosts the playbook will run for, so we just set the
        # variables to exist for all of the hosts in the inventory we were given since
        # the variables won't persist past the lifetime of this playbook anyway
        if vars:
            for varname in vars:
                for host in self._inventory.list_hosts():
                    self._variable_manager.set_host_variable(
                        host=host,
                        varname=varname,
                        value=vars[varname]
                    )

        PlaybookExecutor(
            playbooks=[playbook_source],
            inventory=self._inventory,
            variable_manager=self._variable_manager,
            loader=self._data_loader,
            options=self._ansible_playbook_options,
            passwords=self._passwords
        ).run()
