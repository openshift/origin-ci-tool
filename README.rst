origin-ci-tool
--------------

A CLI tool for building, testing and composing OpenShift repositories.

Installation
------------

 - clone this repository somewhere
 - clone the development branch of Ansible somewhere
 - create a virtualenv for this project using `--system-site-packages` (we need to inherit `yum` from the system)
 - activate it
 - `pip install` Ansible from the local checkout
 - `pip install` this project from the local working directory
 - you're good to go