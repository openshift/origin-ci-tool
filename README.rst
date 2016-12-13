##############
origin-ci-tool
##############

A CLI tool for building, testing and composing OpenShift repositories.

********
Overview
********

The ``origin-ci-tool`` allows for developers to provision virtual machine environments locally using a hypervisor on the
development host and remotely in a cloud computing environment. These environments contain all of the major source code
repositories for the OpenShift ecosystem and can be configured to check out these repositories in whatever state necessary.
Release artifacts can be built from all of these repositories in concert and used to start an OpenShift cluster.

This tool is a successor to `the OpenShift Vagrant plugin <https://github.com/openshift/vagrant-openshift>`_ and is intended to
support a superset of use-cases. Consult the `Sample Use-Cases`_ section to see some examples of specific workflows that are
supported.

Prospective contributors should read the `Contributing`_ section to determine the best way to extend the functionality of this
tool for their needs.

************
Installation
************

Prerequisites
=============

This project requires Python 2 and the ``pip`` package manager for installation. On RHEL, CentOS and Fedora, install them with:

.. code-block:: shell

    $ sudo yum install python2 python-pip

On Mac OS, the preferred method uses `Homebrew <http://brew.sh/>`_. Installation instructions for Homebrew are on `their
website <https://github.com/Homebrew/brew/blob/master/docs/Installation.md#installation>`_. Using Homebrew, install Python (
``brew`` will automatically install ``pip``) with:

.. code-block:: shell

    $ sudo brew install python

On Mac OS, the Python bindings for the AWS API are also necessary:

.. code-block:: shell

    $ pip install boto
    $ pip install boto3

Core Installation
=================

Today, full functionality of this tool requires a development version of Ansible benefit from the following patches:

1. `New ec2_group_facts module to be able to get facts from EC2 security groups <https://github.com/ansible/ansible-modules-extras/pull/2591>`_
2. `Factored polling std{out,err} reads into a function <https://github.com/ansible/ansible/pull/19298>`_
3. `Add support to the make module for targets with options <https://github.com/ansible/ansible/pull/18848>`_
4. `ec2_group_facts: Fail correctly when boto3 is not installed  <https://github.com/ansible/ansible/pull/18842>`_
5. `Only read EC2 regions_exclude list if necessary <https://github.com/ansible/ansible/pull/18720>`_

Due to this requirement, it is highly suggested that you install this tool inside of a virtual environment for Python. To do
so, the ``virtualenv`` package will be necessary. Install it with:

.. code-block:: shell

    $ sudo pip install setuptools virtualenv

Navigate to a directory where the source for Ansible and this tool will live, and clone both using ``git``:

.. code-block:: shell

    $ git clone https://github.com/stevekuznetsov/ansible.git
    $ pushd ansible
    $ git checkout skuznets/oct-release
    $ popd
    $ git clone https://github.com/stevekuznetsov/origin-ci-tool.git

Now, create a virtual environment. In the following examples, the environment is named and created in a directory ``venv``. On
Linux systems, you will want to allow the virtual environment to access system site packages, as running Ansible against the
local host requires Python bindings for ``yum`` and ``dnf``, which cannot be installed in the virtual environment.

.. code-block:: shell

    $ virtualenv venv --system-site-packages

On Mac OS, the virtual environment can be created without this option:

.. code-block:: shell

    $ virtualenv venv

Activate the virtual environment:

.. code-block:: shell

    $ source ./venv/bin/activate

Install Ansible and the ``origin-ci-tool`` in the virtual environment:

.. code-block:: shell

    $ pip install ./ansible
    $ pip install ./origin-ci-tool

You are now ready to use the ``oct`` CLI tool. If you want to use this virtual environment and get access to ``oct`` every time
you open a shell, add the activate line to your ``~/.bashrc``:

.. code-block:: shell

    $ echo "source '$( pwd )/venv/bin/activate'" >> ~/.bashrc

If you want to exit the virtual environment in a shell, use the ``deactivate`` function:

.. code-block:: shell

    $ deactivate

On Linux, some system dependencies are furthermore necessary. Install them using:

.. code-block:: shell

    $ oct bootstrap self

If you wish to develop and package VM images, further dependencies are required and can be installed with:

.. code-block:: shell

    $ oct bootstrap self --for-images

*************
Configuration
*************

The ``origin-ci-tool`` will place a directory of configuration files and runtime metadata to persist state between CLI
invocations. By default, this will be placed at ``~/.config/origin-ci-tool`` but can be configured to be at ``${

AWS Credentials and Configuration
=================================

Communicating with the AWS API to provision virtual machines in EC2 requires a set of credentials. The ``origin-ci-tool`` uses
the same credential store as the AWS CLI. Detailed instructions for configuring the credential file are at the `AWS User Guide
<http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>`_, but the general flow is simple. If you have
the AWS CLI installed, simply run:

.. code-block:: shell

    $ aws configure

If not, you'll want to place a file at ``~/.aws/credentials`` with the following content:

.. code-block:: ini
    :caption: ~/.aws/credentials

    [default]
    aws_access_key_id=XXXXXXXXXXXXXXXXXXXX
    aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

When setting up the SSH configuration for virtual machines provisioned in AWS EC2, the name and location of the private key used
to reach the instance need to be known by the ``origin-ci-tool``. Configure them with:

.. code-block:: shell

    $ oct configure aws-client keypair_name KEY_NAME
    $ oct configure aws-client private_key_path /path/to/KEY_NAME.pem

You can review your configuration with:

.. code-block:: shell

    $ oct configure aws-client --view

****************
Sample Use-Cases
****************

Provisioning an OpenShift Origin Cluster
========================================

Running Tests On Updated Code
=============================

Rebuilding The Ecosystem From Updated Code
==========================================

Creating a VM Image
===================

************
Contributing
************

Design Principles
=================

Integration With New Repositories
=================================

Running Tests
=============

