# coding=utf-8
from __future__ import absolute_import, division, print_function

from __main__ import display
from ansible.cli.playbook import PlaybookCLI
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from click import ClickException
from os.path import abspath

DEFAULT_VERBOSITY = 1


class AnsibleCoreClient(object):
    """
    This is both a container that holds configuration
    options for the Ansible core and a client for the
    Ansible Core, allowing us to run playbooks.
    """

    # Move the comments about the parameters into a doc string
    def __init__(self,
                 inventory_file=None,
                 verbosity=DEFAULT_VERBOSITY,
                 dry_run=False):
        if inventory_file is None:
            # default to the dynamic Vagrant inventory
            from ..vagrant.inventory import __file__ as inventory_full_path
            inventory_file = abspath(inventory_full_path)

        # location of the inventory file to use
        self.host_list = inventory_file
        # verbosity level for Ansible output
        self.verbosity = verbosity
        # whether or not to make changes on the remote host
        self.check = dry_run

    def generate_playbook_options(self, playbook):
        """
        Use the Ansible CLI code to generate a set of options
        for the Playbook API. We do not know or care about the
        fields that may or may not be needed from the options,
        so we let the Ansible code parse them out and set other
        defaults as necessary.

        :return: namedtuple-esque playbook options object
        """
        playbook_args = [
            'ansible-playbook',
            '-{}'.format('v' * self.verbosity),
            playbook
        ]

        if self.check:
            playbook_args.append('--check')

        playbook_cli = PlaybookCLI(args=playbook_args)
        playbook_cli.parse()

        return playbook_cli.options

    def run_playbook(self, playbook_file, playbook_variables=None):
        """
        Run a playbook from file with the variables provided.

        :param playbook_file: the location of the playbook
        :param playbook_variables: extra variables for the playbook
        """
        variable_manager = VariableManager()
        data_loader = DataLoader()
        inventory = Inventory(
            loader=data_loader,
            variable_manager=variable_manager,
            host_list=self.host_list
        )
        variable_manager.set_inventory(inventory)
        variable_manager.extra_vars = playbook_variables

        # until Ansible's display logic is less hack-ey we need
        # to mutate their global in __main__
        options = self.generate_playbook_options(playbook_file)
        display.verbosity = options.verbosity

        result = PlaybookExecutor(
            playbooks=[playbook_file],
            inventory=inventory,
            variable_manager=variable_manager,
            loader=data_loader,
            options=options,
            passwords=None
        ).run()

        if result != TaskQueueManager.RUN_OK:
            raise ClickException('Playbook execution failed with code {}'.format(result))
