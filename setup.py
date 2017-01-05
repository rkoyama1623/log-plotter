#!/usr/bin/env python
from xml.etree import ElementTree
import os

SCRIPTDIR = os.path.abspath(os.path.dirname(__file__))

# setup log_plotter using distutils
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import setup, find_packages
from catkin_pkg.python_setup import generate_distutils_setup
from os.path import join
d=generate_distutils_setup(
    package_xml_path=SCRIPTDIR,
    packages=['log_plotter'],
    package_dir={'': 'src'},
    scripts=['src/log_plotter/datalogger_plotter_with_pyqtgraph.py'],
    # depends=['catkin_pkg', 'pyqtgraph', 'metayaml']
    install_requires=[
        'catkin_pkg',
        'pyqtgraph',
        'metayaml'
    ],
)

# get commit hash
from subprocess import check_output
try:
    GIT_REVISION = check_output(["git", "rev-parse", "HEAD"]).replace("\n","")
except:
    GIT_REVISION = ""
    
# write into version.py
with open(os.path.join(SCRIPTDIR, "src","log_plotter","version.py"),"w") as version_py:
    version_py.writelines("# THIS FILE IS GENERATED FROM LOG_PLOTTER SETUP.PY\n")
    version_py.writelines("version='{}'\n".format(d["version"]))
    version_py.writelines("git_revision='{}'\n".format(GIT_REVISION))

setup(**d)
