# coding=utf-8
# @File  : setup.py
# @Author: PuJi
# @Date  : 2018/5/5 0005

import os
from setuptools import setup,find_packages


requires=[
    'backports-abc==0.5',
    'certifi==2018.4.16',
    'chardet==3.0.4',
    'click==6.7',
    'Flask==0.12.2',
    'Flask-Cors==3.0.3',
    'Flask-SQLAlchemy==2.3.2',
    'futures==3.2.0',
    'idna==2.6',
    'ipfsapi==0.4.2.post1',
    'itsdangerous==0.24',
    'Jinja2==2.10',
    'MarkupSafe==1.0',
    'Naked==0.1.31',
    'passlib==1.7.1',
    'pyasn1==0.4.2',
    'pycryptodome==3.6.1',
    'PyYAML==3.12',
    'requests==2.18.4',
    'rsa==3.4.2',
    'shellescape==3.4.1',
    'singledispatch==3.4.0.3',
    'six==1.11.0',
    'SQLAlchemy==1.2.7',
    'tornado==5.0.2',
    'urllib3==1.22',
    'Werkzeug==0.14.1',
]


base_dir = os.path.abspath(os.path.dirname(__file__))
# Get the long description from the README file
with open(os.path.join(base_dir, 'README.md'), 'rb') as f:
    long_description = f.read().decode('utf-8')

console_scripts = [
    'ulordapi = upapi.src.daemon.daemonCLI:main'
]

package_name = "ulordapi"

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(base_dir),
    author="PuJi",
    author_email="caolinan@ulord.net",
    url="https://ulord.one/",
    description="SDK for the Ulord APIs",
    long_description=long_description,
    keywords="ulord api blockchain",
    license='MIT',
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={'console_scripts': console_scripts},
)