#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Add the above declaration on all python files

from setuptools import setup, find_packages

# Flush this out a bit more
setup(
    name='oct',
    version='0.1',
    url='https://www.github.com/stevekuznetsov/origin-ci-tool',
    maintainer='Steve Kuznetsov',
    maintainer_email='skuznets@redhat.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'ansible',
    ],
    entry_points='''
        [console_scripts]
        oct=oct.oct:oct
    ''',
)
