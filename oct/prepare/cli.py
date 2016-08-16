from collections import namedtuple

import click
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars import VariableManager


@click.group()
def prepare():
    click.echo("placeholder for `prepare` functionality: installing dependencies onto a naked host")


@prepare.command()
def test():
    options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
    # initialize needed objects
    variable_manager = VariableManager()
    loader = DataLoader()
    options = options(connection='local', module_path='/path/to/mymodules', forks=100, become=None, become_method=None,
                      become_user=None, check=False)
    passwords = dict(vault_pass='secret')

    # create inventory and pass to var manager
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='localhost')
    variable_manager.set_inventory(inventory)

    # create play with tasks
    play_source = dict(
        name="Ansible Play",
        hosts='localhost',
        gather_facts='no',
        tasks=[
            dict(action=dict(module='shell', args='ls'), register='shell_out', name='test'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
        ]
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # actually run it
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
        )
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()
