# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import UsageError, argument, command, echo, option, pass_context

_short_help = 'View all or some serialized configuration options.'


@command(
    short_help=_short_help,
    help=_short_help + '''

View the entirety of the serialized configuration options
used by default for Ansible interactions by not passing any
specific options to view. View a specific option or options
by passing option names as arguments.

\b
Examples:
  View all of the configuration options
  $ oct config show
\b
  View the 'verbosity' configuration option
  $ oct config show 'verbosity'
\b
  View the 'check', 'become', and 'verbosity' configuration options
  $ oct config show 'check' 'become' 'verbosity'
'''
)
@option(
    '--all', '-a',
    'show_all',
    help='Print all configuration options.',
    is_flag=True
)
@argument(
    'options',
    nargs=-1
)
@pass_context
def show(context, options, show_all):
    """
    Print a nice representation of the configuration option
    as found in the serialized configuration. If no options
    are specified or if all are requested, print all options.

    :param context: Click context
    :param show_all: whether or not to print all options
    :param options: which options to show the value for
    """
    to_print = {}

    configuration = context.obj
    if options and not show_all:
        for config_option in options:
            if config_option not in configuration:
                raise UsageError(message='Option ' + config_option + ' not found in configuration.')
            else:
                to_print[config_option] = configuration[config_option]
    else:
        for k, v in configuration.items():
            to_print[k] = v

    print_options(to_print)


def print_options(options):
    """
    Print a nice representation of key-value pairs.

    :param options: the key-value pairs to print
    """
    max_length = max([len(repr(key)) for key in options])
    for key in options:
        echo('%*r: %r' % (max_length, str(key), str(options[key])))
