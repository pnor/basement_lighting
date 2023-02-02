#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# from __future__ import absolute_import
# from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


setup(
    name="basement_lighting",
    version="0.1",
    license="",
    description="Mini project to control lights in the basement",
    author="",
    author_email="",
    packages=find_packages("."),
    package_dir={"": "."},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Linux",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    keywords=[
        # eg: 'hobby'
    ],
    python_requires=">=3.9",
    install_requires=[],
    extras_require={},
    sass_manifests={"basement_lighting": ("static/sass", "static/css")},
    setup_requires=["libsass >= 0.6.0"],
    entry_points={
        "console_scripts": [
            #            "api = api.api:main",
            "par = parametric.fill:main",
        ]
    },
)
