#!/usr/bin/env python3

from setuptools import find_packages, setup
import setuptools.command.build_py
import tarfile
import urllib.request

# NOTE(cutwater): Because bindings are statically generated, requirements list
#   from pulp-galaxy/setup.py has to be copied here and manually maintained.
galaxy_pulp_requirements = [
    "urllib3 >= 1.15",
    "six >= 1.10",
    "certifi",
    "python-dateutil"
]

requirements = galaxy_pulp_requirements + [
    "Django~=2.2.3",
    "pulpcore>=3.1.1",
    "pulp-ansible>=0.2.0b8",
    "django-prometheus>=2.0.0",
    "django-storages[boto3]",
]


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        print('Downloading UI static files')

        download_url = 'https://github.com/ansible/ansible-hub-ui/' + \
            'releases/latest/download/automation-hub-ui-dist.tar.gz'

        filename, headers = urllib.request.urlretrieve(
            download_url,
            'automation-hub-ui-dist.tar.gz'
        )

        print('Extracting ' + filename)
        tarfile.open(filename).extractall(
            path='galaxy_ng/app/static/galaxy_ng'
        )

        setuptools.command.build_py.build_py.run(self)


setup(
    name="galaxy-ng",
    version="0.1.0a1",
    description="galaxy-ng plugin for the Pulp Project",
    license="GPLv2+",
    author="AUTHOR",
    author_email="author@email.here",
    url="http://example.com/",
    python_requires=">=3.6",
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ),
    entry_points={"pulpcore.plugin": ["galaxy_ng = galaxy_ng:default_app_config"]},
    cmdclass={
        'build_py': BuildPyCommand,
    },
)
