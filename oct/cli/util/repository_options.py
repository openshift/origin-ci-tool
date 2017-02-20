# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Choice, argument


class Repository(object):
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
    online = 'online'
    release = 'release'
    aoscdjobs = 'aos-cd-jobs'
    openshift_ansible = 'openshift-ansible'


def repository_argument(func):
    """
    Add the repository selection argument to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return argument(
        'repository', nargs=1, type=Choice([
            Repository.origin,
            Repository.enterprise,
            Repository.web_console,
            Repository.source_to_image,
            Repository.metrics,
            Repository.logging,
            Repository.online,
            Repository.release,
            Repository.aoscdjobs,
            Repository.openshift_ansible,
        ])
    )(func)
