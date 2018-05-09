# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import Choice, option


class OperatingSystem(object):
    """
    An enumeration of supported operating systems for
    Vagrant provisioning of VMs.
    """
    fedora = 'fedora'
    centos = 'centos'
    rhel = 'rhel'


class Stage(object):
    """
    An enumeration of supported stages for images used
    for provisioning of VMs.
    """
    bare = 'bare'
    base = 'base'
    build = 'build'
    install = 'install'
    fork = 'fork'
    crio = 'crio'
    ose_master = 'ose-master'
    ose_enterprise_39 = 'ose-enterprise-3.9'
    ose_enterprise_38 = 'ose-enterprise-3.8'
    ose_enterprise_37 = 'ose-enterprise-3.7'
    ose_enterprise_36 = 'ose-enterprise-3.6'


def operating_system_option(func):
    """
    Add option to decorated command func for specifying OperatingSystem

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--os',
        '-o',
        'operating_system',
        type=Choice([
            OperatingSystem.fedora,
            OperatingSystem.centos,
            OperatingSystem.rhel,
        ]),
        show_default=True,
        metavar='NAME',
        help='VM operating system.',
    )(func)


def stage_option(func):
    """
    Add option to decorated command func for specifying image build Stage

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--stage',
        '-s',
        type=Choice([
            Stage.bare,
            Stage.base,
            Stage.build,
            Stage.install,
            Stage.fork,
            Stage.crio,
            Stage.ose_master,
            Stage.ose_enterprise_39,
            Stage.ose_enterprise_38,
            Stage.ose_enterprise_37,
            Stage.ose_enterprise_36,
        ]),
        # default=Stage.install,
        show_default=True,
        metavar='NAME',
        help='VM image stage.',
    )(func)


def ami_id_option(func):
    """
    Add option to decorated command func for specifying unique AWS AMI identifier

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return option(
        '--ami-id',
        '-a',
        'ami_id',
        metavar='ID',
        help='AWS AMI identifier.',
    )(func)
