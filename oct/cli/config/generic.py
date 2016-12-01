# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import ClickException, argument, command, echo, option, pass_context

_short_help = 'Update or view the {} configuration.'


def configuration_options(name, container, use, example_key, example_value, fetch_func):
    """
    Get a decorator for configuration modification options.

    :param name: name of the command
    :param container: the name of the configuration to work on
    :param use: usage string for the configuration options
    :param example_key: example update key
    :param example_value: example update value
    :param fetch_func: function to get container from the context
    :return: the decorator for the CLI function
    """

    def configuration_options_decorator(func):
        def view_configuration(context, _, value):
            """
            View the configuration options for a container. Handles
            the `--view` option.

            :param context: Click context
            :param _: command-line parameter
            :param value: whether or not to view the configuration
            """
            if not value or context.resilient_parsing:
                return

            config_container = fetch_func(context)
            max_length = max([len(key) for key in config_container])
            for key in config_container:
                echo('{:>{width}s}: {}'.format(key, config_container[key], width=max_length))

            context.exit()

        click_options = [
            command(
                name=name,
                short_help=_short_help.format(container),
                help=_short_help.format(container) + '''

Existing configuration options that are used to {use}
can be edited with this command.

\b
Examples:
  Update the option '{key}' option to '{value}'
  $ oct configure {name} '{key}' '{value}'
\b
  View the current {container}options
  $ oct configure {name} --view
'''.format(name=name, container=container, use=use, key=example_key, value=example_value)
            ),
            argument(
                'option'
            ),
            argument(
                'value'
            ),
            option(
                '--view', '-v',
                help='Print all configuration options.',
                is_flag=True,
                callback=view_configuration
            ),
            pass_context
        ]

        for click_option in reversed(click_options):
            func = click_option(func)

        return func

    return configuration_options_decorator


def update_configuration_option(container, option, value, write_func):
    """
    Update an option in a configuration file.

    :param container: configuration file to work on
    :param option: name of the option to update
    :param value: value to update to
    :param write_func: func to serialize the updated config
    """
    if option not in container:
        raise ClickException(message='Option {} not found in configuration.'.format(option))

    setattr(container, option, value)
    write_func()

    echo('Option {} updated to be {}.'.format(option, value))
