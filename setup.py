#!/usr/bin/env python
from xml.etree import ElementTree
import os

VERSION=ElementTree.parse("package.xml").getroot().find("version").text
SCRIPTDIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(SCRIPTDIR, "src/log_plotter/version.py"),"w") as version_py:
    version_py.writelines("# THIS FILE IS GENERATED FROM NUMPY SETUP.PY\n")
    version_py.writelines("version='{}'".format(VERSION))

try: # install in catkin work space
    from distutils.core import setup
    from catkin_pkg.python_setup import generate_distutils_setup

    d = generate_distutils_setup(
        packages=['log_plotter'],
        package_dir={'': 'src'},
        scripts=['src/log_plotter/datalogger_plotter_with_pyqtgraph.py'],
    )
    setup(**d)
except: # install in /usr/local/
    print('catkin is not installed. use setuptools instead')
    from setuptools import setup, find_packages
    from os.path import join
    setup(name='log_plotter',
          version=VERSION,
          description='log plotter for hrpsys',
          packages=[join('src', package) for package in find_packages(where='./src/')],
          entry_points="""
          [console_scripts]
          datalogger-plotter-with-pyqtgraph = log_plotter:main
          """,)

