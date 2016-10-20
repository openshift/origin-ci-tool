# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import group, pass_context

from .cli.bootstrap.group import bootstrap
from .cli.build.group import build
from .cli.config.group import configure
from .cli.install.group import install
from .cli.make.make import make
from .cli.package.group import package
from .cli.prepare.group import prepare
from .cli.provision.group import provision
from .cli.sync.group import sync
from .cli.test.group import test
from .cli.version import version
from .config.configuration import Configuration


@group(
    name='oct',
    help='''
A CLI tool for building, testing and composing OpenShift repositories.
'''
)
@pass_context
def oct_command(context):
    """
    Load the on-disk configuration and save it in the
    Click context so that children of this root command
    will have access to it.
    """
    context.obj = Configuration()


oct_command.add_command(bootstrap)
oct_command.add_command(build)
oct_command.add_command(configure)
oct_command.add_command(install)
oct_command.add_command(make)
oct_command.add_command(prepare)
oct_command.add_command(package)
oct_command.add_command(provision)
oct_command.add_command(sync)
oct_command.add_command(test)
oct_command.add_command(version)
