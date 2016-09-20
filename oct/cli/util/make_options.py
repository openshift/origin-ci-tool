import click


def make_options(func):
    """
    Add all of the make options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    options = [
        make_target_argument,
        make_parameter_option,
        make_directory_override_option
    ]

    for option in reversed(options):
        func = option(func)

    return func


def make_target_argument(func):
    """
    Add the make target argument to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.argument(
        'target',
        nargs=-1,
        required=True
    )(func)


def make_parameter_option(func):
    """
    Add the make parameter option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--env', '-e',
        'parameters',
        metavar='KEY=VAL',
        multiple=True,
        help='Parameter key-value-pair.'
    )(func)


def make_directory_override_option(func):
    """
    Add the make destination option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--dest', '-d',
        'make_destination',
        type=click.Path(
            file_okay=False,
            dir_okay=True
        ),
        help='Remote directory to run make in. Optional.'
    )(func)
