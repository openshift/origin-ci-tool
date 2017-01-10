# coding=utf-8
from __future__ import absolute_import, division, print_function

from functools import partial
from time import sleep
from os import environ, mkdir
from os.path import abspath, dirname, exists, join

from __main__ import display  # pylint: disable=no-name-in-module
from ansible import constants
from ansible.cli.playbook import PlaybookCLI
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.plugins import callback_loader
from ansible.vars import VariableManager
from click import ClickException

DEFAULT_VERBOSITY = 1


class AnsibleCoreClient(object):
    """
    This is both a container that holds configuration
    options for the Ansible core and a client for the
    Ansible Core, allowing us to run playbooks.
    """

    def __init__(
            self,
            inventory_dir,
            verbosity=DEFAULT_VERBOSITY,
            dry_run=False,
            log_directory=None,
            custom_module_path=None,
    ):
        if custom_module_path is None:
            # default to the pre-packaged custom module path
            from ..oct import __file__ as base_directory
            custom_module_path = join(abspath(dirname(base_directory)), 'ansible', 'oct', 'library')

        # location of the inventory directory to use
        self.host_list = inventory_dir
        # verbosity level for Ansible output
        self.verbosity = verbosity
        # whether or not to make changes on the remote host
        self.check = dry_run
        # where to store logs for Ansible playbooks
        self.log_directory = log_directory
        # from where to load custom Ansible modules
        self.custom_module_path = custom_module_path

    def __iter__(self):
        """
        Return an iterator for contained properties.

        :return: the iterator
        """
        return (x for x in vars(self))

    def __getitem__(self, key):
        """
        Fetch the configuration key.

        :param key: name of the item to fetch
        :return: value of the item
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError('No such option `{}`.'.format(key))

    def __setitem__(self, key, value):
        """
        Update the value of the configuration entry.

        :param key: name of the item to update
        :param value: value to update the item to
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError('No such option `{}`.'.format(key))

    def __contains__(self, key):
        """
        Determine if the container in fact
        contain the configuration item.

        :param key: name of the item to search for
        :return: whether or not we contain the item
        """
        return hasattr(self, key)

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
            playbook,
        ]

        if self.check:
            playbook_args.append('--check')

        playbook_cli = PlaybookCLI(args=playbook_args)
        playbook_cli.parse()

        playbook_cli.options.module_path = self.custom_module_path

        return playbook_cli.options

    def run_playbook(self, playbook_file, playbook_variables=None, option_overrides=None):
        """
        Run a playbook from file with the variables provided.

        :param playbook_file: the location of the playbook
        :param playbook_variables: extra variables for the playbook
        """
        # on the first run, the playbook that initializes the
        # inventory will not have yet run, so we should ensure
        # that the directory for it exists, at the least, so
        # ansible doesn't complain
        if not exists(self.host_list):
            mkdir(self.host_list)

        variable_manager = VariableManager()
        data_loader = DataLoader()
        inventory = Inventory(
            loader=data_loader,
            variable_manager=variable_manager,
            host_list=self.host_list,
        )
        variable_manager.set_inventory(inventory)
        variable_manager.extra_vars = playbook_variables

        # until Ansible's display logic is less hack-ey we need
        # to mutate their global in __main__
        options = self.generate_playbook_options(playbook_file)
        display.verbosity = options.verbosity

        # we want to log everything so we can parse output
        # nicely later from files and don't miss output due
        # to the pretty printer, if it's on
        from ..oct import __file__ as root_dir
        callback_loader.add_directory(join(dirname(root_dir), 'ansible', 'oct', 'callback_plugins'))
        constants.DEFAULT_CALLBACK_WHITELIST = ['log_results', 'generate_junit']
        environ['ANSIBLE_LOG_ROOT_PATH'] = self.log_directory

        if options.verbosity == 1:
            # if the user has not asked for verbose output
            # we will use our pretty printer for progress
            # on the TTY
            constants.DEFAULT_STDOUT_CALLBACK = 'pretty_progress'

            # we really don't want output in std{err,out}
            # that we didn't put there, but some code in
            # Ansible calls directly to the Display, not
            # through a callback, so we need to ensure
            # that those raw calls don't go to stdout
            display.display = partial(display.display, log_only=True)
        else:
            # if the user asks for verbose output, we want
            # to give them nicer output than the default
            # plugin, anyway
            constants.DEFAULT_STDOUT_CALLBACK = 'default_with_output_lists'

        if option_overrides:
            for key in option_overrides:
                if hasattr(options, key):
                    setattr(options, key, option_overrides[key])

        result = PlaybookExecutor(
            playbooks=[playbook_file],
            inventory=inventory,
            variable_manager=variable_manager,
            loader=data_loader,
            options=options,
            passwords=None,
        ).run()

        if result != TaskQueueManager.RUN_OK:
            # TODO: this seems bad, but can we discover the thread here to join() it?
            sleep(0.2)
            raise ClickException('Playbook execution failed with code ' + str(result))
