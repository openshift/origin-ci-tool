# coding=utf-8
from oct.cli.version import VERSION
from setuptools import find_packages, setup

base_requires = [
    'Click',
    'ansible',
    'backports.shutil_get_terminal_size'
]

setup(
    name='oct',
    version=VERSION,
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
