from distutils.core import setup
from setuptools import find_packages


PACKAGE_NAME = "input-monitor"
PACKAGE_VERSION = "1.0.0"
MAINTAINER = "Morning Team"
MAINTAINER_EMAIL = "no-reply@morning.team"
URL = "https://morning.team"


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    packages=find_packages(),
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
