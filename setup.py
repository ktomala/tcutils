# -*- coding: utf-8 -*-

"""Setup for tcutils."""

from setuptools import setup, find_packages
# from babel.messages import frontend as babel


# with open('README.rst') as f:
#     readme = f.read()
#
# with open('LICENSE') as f:
#     license = f.read()

install_requires = [
    'pyyaml',
    'marshmallow'
]

setup(
    name='tcutils',
    version='0.1.1',
    description='TropiCoders Utility Library',
    # long_description=readme,
    author='Karol Tomala',
    author_email='ktomala@tropicoders.pl',
    # url='https://your_project.com',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    # cmdclass={
    #     'compile_catalog': babel.compile_catalog,
    #     'extract_messages': babel.extract_messages,
    #     'init_catalog': babel.init_catalog,
    #     'update_catalog': babel.update_catalog
    # }
    # python_requires='>=3.6',
    install_requires=install_requires,
    # dependency_links=dependencies,
)
