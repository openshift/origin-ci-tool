import click
from __future__ import absolute_import, division, print_function


class Repository:
    """
    An enumeration of repository names that are currently
    supported as a part of the OpenShift ecosystem.
    """
    origin = 'origin'
    enterprise = 'ose'
    web_console = 'origin-web-console'
    source_to_image = 'source-to-image'
    metrics = 'origin-metrics'
    logging = 'origin-aggregated-logging'


def repository_argument(func):
    """
    Add the repository selection argument to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.argument(
        'repository',
        nargs=1,
        type=click.Choice([
            Repository.origin,
            Repository.enterprise,
            Repository.web_console,
            Repository.source_to_image,
            Repository.metrics,
            Repository.logging
        ])
    )(func)
