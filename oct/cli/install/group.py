from __future__ import absolute_import, division, print_function

from click import echo, group


@group(
    short_help='Install and configure systems from binaries and artifacts.'
)
def install():
    echo("placeholder for `install` functionality: installing binaries/RPMs/images")
