# coding=utf-8
# @File  : setup.py
# @Author: PuJi
# @Date  : 2018/5/5 0005


import os, shutil,platform
import site
from setuptools import setup,find_packages
from distutils.sysconfig import get_python_lib
from ulordapi.version import __py_version__, __packagename__

requires2=[
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
requires3=[
    'certifi==2018.4.16',
    'chardet==3.0.4',
    'click==6.7',
    'Flask==1.0.2',
    'Flask-Cors==3.0.6',
    'Flask-SQLAlchemy==2.3.2',
    'idna==2.7',
    'ipfsapi==0.4.3',
    'itsdangerous==0.24',
    'Jinja2==2.10',
    'MarkupSafe==1.0',
    'requests==2.19.1',
    'six==1.11.0',
    'SQLAlchemy==1.2.9',
    'urllib3==1.23',
    'Werkzeug==0.14.1',
]

# about = {}
# here = os.path.abspath(os.path.dirname(__file__))

# with open(os.path.join(here, 'ulordapi', '__version__.py'), 'r', 'utf-8') as f:
#     exec(f.read(), about)


base_dir = os.path.abspath(os.path.dirname(__file__))
# Get the long description from the README file
with open(os.path.join(base_dir, 'readme.md'), 'rb') as f:
    long_description = f.read().decode('utf-8')

if 2 <= __py_version__ < 3:
    requires = requires2
elif 3 <= __py_version__ < 4:
    requires = requires3
else:
    print("error python version")
    exit(-1)

setup(
    name="ulordapi",
    # version=about['__version__'],
    version='0.0.1',
    packages=find_packages(base_dir),
    author="PuJi",
    author_email="caolinan@ulord.net",
    url="https://github.com/UlordChain/py-ulord-api",
    description="SDK for the Ulord APIs",
    long_description=long_description,
    keywords="ulord api blockchain",
    license='MIT',
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ulordapi = ulordapi.daemonCLI:main'
        ]},
    Platform=['win32','linux'],
    # python_requires='>=2.6, <3',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: both',
    ]
)

current_place = get_python_lib()
dst = None #  tool dir
try:
    lib_paths = site.getsitepackages()
    for lib_path in lib_paths:
        if os.path.isdir(os.path.join(lib_path, __packagename__)):
            # current python lib path
            dst = os.path.join(lib_path, __packagename__, 'ulordapi', 'udfs', 'tools')
except:
    # venv path
    # import platform
    # if platform.system() in ["Windows", "Win32"]:
    #     print(""current os is windows)
    # print("current python using venv")
    dst = os.path.join(current_place, __packagename__, 'ulordapi', 'udfs', 'tools')

if not dst:
    dst = os.path.join(current_place, __packagename__, 'ulordapi', 'udfs', 'tools')
try:
    os.stat(dst)
except:
    try:
        os.makedirs(dst)
    except Exception as e:
        print(e)
if platform.system().startswith('Win'):
    shutil.copy2(os.path.join('ulordapi', 'udfs', 'tools', 'udfs.exe'),
                 os.path.join(dst, 'udfs.exe'))
else:
    shutil.copy2(os.path.join('ulordapi', 'udfs', 'tools', 'udfs'),
                    os.path.join(dst, 'udfs'))
    # change udfs stat
    import stat
    os.chmod(os.path.join(dst, 'udfs'), stat.S_IXOTH)

