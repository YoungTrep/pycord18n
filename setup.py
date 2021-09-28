# Copyright (C) 2021 YoungTrep
#
# This file is part of pycord18n.
#
# pycord18n is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pycord18n is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pycord18n.  If not, see <http://www.gnu.org/licenses/>.

import re
from os import path
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requirements = []
with open("requirements.txt") as rtxt:
    requirements = rtxt.read().splitlines()

version = ""
with open("pycord18n/__init__.py") as initpy:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', initpy.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Version is not set!')

setup(name='pycord18n',
      version=version,
      author='YoungTrep, Ghoul',
      author_email='youngtrep.business@gmail.com',
      description='Localization for the discord.py fork, pycord',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/YoungTrep/pycord18n',
      project_urls={
          'Issue Tracker': 'https://github.com/YoungTrep/pycord18n/issues'
      },
      packages=['pycord18n'],
      license='GNU',
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Natural Language :: English'
      ],
      python_requires='>=3.6',
      install_requires=requirements
)
