__author__ = "Omer Yampel @yampelo"

import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command


# Package meta-data.
NAME = "pybeagle"
DESCRIPTION = "Beagle is an incident response and digital forensics tool which transforms data sources and logs into graphs"
URL = "https://github.com/yampelo/beagle"
AUTHOR = "yampelo"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "1.0.5"
EMAIL = None

splunk = ["splunk-sdk==1.6.6"]
rekall = ["rekall==1.7.2rc1"]
pcap = ["scapy==2.4.3"]
elasticsearch = ["elasticsearch==7.1.0"]

_all = splunk + rekall + pcap + elasticsearch
EXTRAS = {"all": _all, "rekall": rekall, "splunk": splunk, "pcap": pcap, "elasticsearch": elasticsearch}
REQUIRED = [
    "ansimarkup==1.4.0",
    "atomicwrites==1.3.0",
    "attrs==19.1.0",
    "better-exceptions-fork==0.2.1.post6",
    "certifi==2019.3.9",
    "chardet==3.0.4",
    "click==7.0",
    "colorama==0.4.1",
    "coverage==5.0a4",
    "decorator==4.4.0",
    "flask-sqlalchemy==2.3.2",
    "flask==1.0.2",
    "Flask-Cors==3.0.8",
    "future==0.16.0",
    "graphistry[networkx]==0.9.63",
    "grpcio==1.20.0rc3",
    "gunicorn==19.9.0",
    "hexdump==3.3",
    "idna==2.8",
    "itsdangerous==1.1.0",
    "jinja2==2.10.1",
    "loguru==0.2.5",
    "lxml==4.3.3",
    "markupsafe==1.1.1",
    "more-itertools==7.0.0 ; python_version > '2.7'",
    "neo4j==1.7.2",
    "neobolt==1.7.4",
    "neotime==1.7.4",
    "networkx==2.3",
    "numpy==1.16.2",
    "pandas==0.24.2",
    "pluggy==0.9.0",
    "protobuf==3.6.1",
    "py==1.8.0",
    "pydgraph==1.0.3",
    "pygments==2.3.1",
    "pytest-cov==2.6.1",
    "pytest==4.4.0",
    "python-dateutil==2.8.0",
    "python-evtx==0.6.1",
    "pytz==2018.9",
    "requests==2.21.0",
    "six==1.12.0",
    "sqlalchemy==1.3.2",
    "urllib3==1.24.1",
    "werkzeug==0.15.3",
    "mock==3.0.5",
]


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.

about = {}  # type: ignore

if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []  # type: ignore

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["test*", "beagle/web"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Security",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
