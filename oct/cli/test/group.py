# coding=utf-8
from __future__ import absolute_import, division, print_function

from click import echo, group


@group(
    short_help='Run tests and other tasks for a synchronized repository.'
)
def test():
    echo("placeholder for `test` functionality: shelling out to Makefiles for actions after builds/installs")
