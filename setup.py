# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

"""Setup for tcutils."""

from setuptools import setup, find_packages
# from babel.messages import frontend as babel


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

install_requires = [
    'pyyaml',
    'marshmallow',
    'click',
]

setup(
    name='tcutils',
    version='0.2.0',
    description='TropiCoders Utility Library',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Karol Tomala',
    author_email='ktomala@tropicoders.pl',
    url='https://github.com/ktomala/tcutils',
    license='MPL 2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    # cmdclass={
    #     'compile_catalog': babel.compile_catalog,
    #     'extract_messages': babel.extract_messages,
    #     'init_catalog': babel.init_catalog,
    #     'update_catalog': babel.update_catalog
    # }
    python_requires='>=3.6',
    install_requires=install_requires,
    # dependency_links=dependencies,
)
