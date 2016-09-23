from setuptools import setup, find_packages

from oct.cli.version import VERSION

setup(
    name='oct',
    version=VERSION,
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
