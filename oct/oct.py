# Ansible Python API currently is not well formed for
# consumers that want to set display attributes like
# the verbosity, so we need to make sure we are the
# first to place a `display` attr in `__main__` so we
# control it later when we want to update things
import __main__
from ansible.utils.display import Display

setattr(__main__, 'display', Display())

import click
from cli.build.group import build
from cli.config.group import config
from cli.install.group import install
from cli.prepare.group import prepare
from cli.provision.group import provision
from cli.sync.group import sync
from cli.test.group import test


@click.group(
    help='''
A CLI tool for building, testing and composing OpenShift repositories.
'''
)
def oct():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


oct.add_command(build)
oct.add_command(config)
oct.add_command(install)
oct.add_command(prepare)
oct.add_command(provision)
oct.add_command(sync)
oct.add_command(test)
