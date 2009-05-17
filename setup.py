#!/usr/bin/env python
#    XXX - converts ODF files from a YUSCII font-encoding to proper UTF-8.
#    Copyright (C) 2009 Damjan Georgievski 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''The setup and build script for the XXX library.'''
__author__ = 'Damjan Georgievski'
__version__ = '1.0'


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
    name = 'XXX',
    version = __version__,
    author = __author__,
    author_email = 'gdamjan@gmail.com',
    description = 'converts ODF files from a YUSCII font-encoding to proper UTF-8',
    license = 'AGPL 3.0',
    url = 'FIXME',
    packages = ['convertor'],
    package_data = {},
    keywords = "ODF",
)


# Extra package metadata to be used only if setuptools is installed
SETUPTOOLS_METADATA = dict(
    install_requires = ['lxml'],
    include_package_data = True,
    classifiers = [
    ],
    test_suite = '',
    zip_safe = False,
    entry_points = """ """
)

# Use setuptools if available, otherwise fallback and use distutils
try:
    import setuptools
    METADATA.update(SETUPTOOLS_METADATA)
    setuptools.setup(**METADATA)
except ImportError:
    import distutils.core
    distutils.core.setup(**METADATA)
