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
    web_console_server = 'origin-web-console-server'
    source_to_image = 'source-to-image'
    metrics = 'origin-metrics'
    logging = 'origin-aggregated-logging'
    online = 'online'
    online_hibernation = 'online-hibernation'
    release = 'release'
    aoscdjobs = 'aos-cd-jobs'
    openshift_ansible = 'openshift-ansible'
    jenkins = 'jenkins'
    wildfly = 'sti-wildfly'
    jenkins_plugin = 'jenkins-plugin'
    jenkins_sync_plugin = 'jenkins-sync-plugin'
    jenkins_client_plugin = 'jenkins-client-plugin'
    jenkins_login_plugin = 'jenkins-openshift-login-plugin'
    image_registry = 'image-registry'
    cluster_operator = 'cluster-operator'
    kubernetes_metrics_server = 'kubernetes-metrics-server'
    online_console_extensions = 'online-console-extensions'
    image_inspector = 'image-inspector'
    online_registration = 'online-registration'
    service_catalog = 'service-catalog'


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
            Repository.web_console_server,
            Repository.source_to_image,
            Repository.metrics,
            Repository.logging,
            Repository.online,
            Repository.online_hibernation,
            Repository.release,
            Repository.aoscdjobs,
            Repository.openshift_ansible,
            Repository.jenkins,
            Repository.wildfly,
            Repository.jenkins_plugin,
            Repository.jenkins_sync_plugin,
            Repository.jenkins_client_plugin,
            Repository.jenkins_login_plugin,
            Repository.image_registry,
            Repository.cluster_operator,
            Repository.kubernetes_metrics_server,
            Repository.online_console_extensions,
            Repository.image_inspector,
            Repository.online_registration,
            Repository.service_catalog,
        ])
    )(func)
