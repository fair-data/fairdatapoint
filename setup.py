#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

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
    name='fairdatapoint',
    version=version['__version__'],
    description="Python implementation of FAIR Data Point",
    long_description=readme + '\n\n',
    long_description_content_type='text/markdown',
    author="Rajaram Kaliyaperumal, Arnold Kuzniar, Cunliang Geng, Carlos Martinez-Ortiz",
    author_email='c.martinez@esciencecenter.nl',
    url='https://github.com/NLeSC/fairdatapoint',
    packages=find_packages(),
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords=['fdp', 'fairdatapoint'],
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
    extras_require={
        'dev': ['prospector[with_pyroma]', 'yapf', 'isort', 'swagger-ui-bundle>=0.0.2'],
        'tests': ['pytest>5.0', 'pytest-cov', 'coveralls', 'pytest-datadir-ng'],
        'docs': ['sphinx', 'sphinx_rtd_theme', 'recommonmark'],
    },
    scripts=[
        'bin/fdp-run'
    ],
)
