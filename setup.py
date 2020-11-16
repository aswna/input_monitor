#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


PACKAGE_NAME = "input-monitor"
PACKAGE_VERSION = "1.0.4"
MAINTAINER = "Morning Team"
MAINTAINER_EMAIL = "no-reply@morning.team"
URL = "https://github.com/aswna/input_monitor"


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "input-monitor-client=input_monitor.input_monitor_client:main",
            "input-monitor-service=input_monitor.input_monitor_service:main",
        ]
    },
    install_requires=[
        "pyinotify",
        "prettytable",
    ]
)
