# coding=utf-8
from __future__ import absolute_import, division, print_function
from click import echo


def quiet_echo(quiet, msg):
    """
    Optionally output a message via click.echo

    :param quiet: suppress output if True
    :param msg: string to output
    """
    if not quiet:
        echo(msg)
