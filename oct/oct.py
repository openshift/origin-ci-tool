# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group

from .cli.bootstrap.group import bootstrap
from .cli.build.group import build
from .cli.config.group import config
from .cli.install.group import install
from .cli.make.make import make
from .cli.prepare.group import prepare
from .cli.provision.group import provision
from .cli.sync.group import sync
from .cli.test.group import test
from .cli.version import version


@group(
    name='oct',
    help='''
A CLI tool for building, testing and composing OpenShift repositories.
'''
)
def oct_command():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


oct_command.add_command(bootstrap)
oct_command.add_command(build)
oct_command.add_command(config)
oct_command.add_command(install)
oct_command.add_command(make)
oct_command.add_command(prepare)
oct_command.add_command(provision)
oct_command.add_command(sync)
oct_command.add_command(test)
oct_command.add_command(version)
