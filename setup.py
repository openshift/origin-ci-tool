# coding=utf-8
from setuptools import setup, find_packages

from oct.cli.version import __version__

base_requires = [
    'Click',
    'ansible'
]

# You still haven't filled setup out
# https://docs.python.org/2/distutils/setupscript.html#additional-meta-data
# https://github.com/ansible/ansible/blob/devel/setup.py#L16
# https://github.com/kennethreitz/requests/blob/master/setup.py#L62
setup(
    name='oct',
    version=__version__,
    url='https://www.github.com/stevekuznetsov/origin-ci-tool',
    maintainer='Steve Kuznetsov',
    maintainer_email='skuznets@redhat.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=base_requires,
    tests_require=base_requires + [
        'mock',
        'coverage'
    ],
    entry_points='''
        [console_scripts]
        oct=oct.oct:oct_command
    ''',
)
