from __future__ import absolute_import, division, print_function

from __main__ import display
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from click import ClickException

from ..config.options import default_inventory, default_options
from ..config.variables import default_variables


class PlaybookRunner(object):
    '''
    This class allows for a simple abstraction around the loading
    and execution of an Ansible playbook given an inventory and
    variables to expose to the playbook.
    '''

    def __init__(self,
                 variable_manager=VariableManager(), data_loader=DataLoader(),
                 # options that we can default from config
                 become=None,
                 become_method=None,
                 become_user=None,
                 check=None,
                 connection=None,
                 forks=None,
                 host_list=None,
                 module_path=None,
                 passwords=None,
                 verbosity=None
                 ):
        """
        Initialize a PlaybookRunner.

        :param verbosity: verbosity level with which to run Ansible
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

        self._ansible_options = default_options({
            'connection': connection,
            'module_path': module_path,
            'forks': forks,
            'become': become,
            'become_method': become_method,
            'become_user': become_user,
            'check': check,
            'verbosity': verbosity,
            'listhosts': None,
            'listtasks': None,
            'listtags': None,
            'syntax': None
        })

        display.verbosity = self._ansible_options.verbosity

        self._passwords = passwords
        self._inventory = Inventory(
            loader=self._data_loader,
            variable_manager=self._variable_manager,
            host_list=default_inventory(host_list)
        )
        self._variable_manager.set_inventory(self._inventory)

    def run(self, playbook_source, playbook_variables=None):
        """
        Run a playbook defined in the file at playbook_source with the variables provided.

        :param playbook_source: the location of the playbook to run
        :param playbook_variables: a dictionary of variables to pass to the playbook
        """
        playbook_variables = default_variables(playbook_variables)
        self._variable_manager.extra_vars = playbook_variables

        result = PlaybookExecutor(
            playbooks=[playbook_source],
            inventory=self._inventory,
            variable_manager=self._variable_manager,
            loader=self._data_loader,
            options=self._ansible_options,
            passwords=self._passwords
        ).run()

        if result is not TaskQueueManager.RUN_OK:
            raise ClickException('Playbook execution failed with code ' + str(result))
