#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit fdp/__version__.py
version = {}
with open(os.path.join(here, 'fdp', '__version__.py')) as f:
    exec(f.read(), version)

with open('requirements.txt', mode='r') as f:
    install_requires = f.read().splitlines()

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='fdp',
    version=version['__version__'],
    description="Python implementation of FAIR Data Point",
    long_description=readme + '\n\n',
    long_description_content_type='text/markdown',
    author="Carlos Martinez-Ortiz",
    author_email='c.martinez@esciencecenter.nl',
    url='https://github.com/NLeSC/fdp',
    packages=[
        'fdp',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='fdp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    install_requires=install_requires,
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort'],
    }
)
