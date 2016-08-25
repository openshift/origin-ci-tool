from setuptools import setup, find_packages

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
