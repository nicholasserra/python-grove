#!/usr/bin/env python

from setuptools import setup

setup(
    name='python-grove',
    version='0.0.1',
    install_requires=[],
    author='Nicholas Serra',
    author_email='nick@528hazelwood.com',
    license='MIT License',
    url='https://github.com/nicholasserra/python-grove/',
    keywords='python grove grove.io http irc api',
    description='A python class to interface with the Grove.io HTTP API',
    long_description=open('README.md').read(),
    download_url="https://github.com/nicholasserra/python-grove/zipball/master",
    py_modules=["grove"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet'
    ]
)