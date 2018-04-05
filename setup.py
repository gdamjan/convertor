#!/usr/bin/env python
#    "convertor" - converts ODF files from a YUSCII font-encoding to proper UTF-8.
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
import setuptools

__author__ = 'Damjan Georgievski'
__version__ = '2.0'
__email__ = 'gdamjan@gmail.com'

setuptools.setup(
    name = 'convertor',
    version = __version__,
    author = __author__,
    author_email = __email__,
    description = 'converts ODF files from a YUSCII font-encoding to proper UTF-8 ODF',
    license = 'AGPL 3.0',
    url = 'http://github.com/gdamjan/convertor',
    packages = ['convertor'],
    package_data = {},
    keywords = "ODF",
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite = '',
    zip_safe = False,
    entry_points = {
        'console_scripts':
            ['convertor=convertor.__main__:main']
    },
    install_requires = ['lxml'],
    extras_require = {
        "web": "Werkzeug"
    }
)
