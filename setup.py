#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This file is part of "pamOIDC-python"
#
# Copyright 2013 Nomura Research Institute, Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

######################################################
NAME = 'pamOIDC-python'
LICENSE = 'Apache License, Version 2.0'
DESCRIPTION = 'libpam-python extension for OpenID Connect'
PACKAGES = ['pamOIDC', ]
AUTHOR = "NRI"
AUTHOR_EMAIL = "oidc@nri.co.jp"
URL = "https://bitbucket.org/PEOFIAMP/pamOIDC-python"
######################################################
import sys
import os
import glob
sys.path.insert(0, os.path.abspath('lib'))

from setuptools import setup

# - Meta Info

from djado import get_version

SCRIPTS = glob.glob('scripts/*')
try:
    INSTALL_REQUIRES = [
        r for r in
        open('requirements.txt').read().split('\n')
        if len(r) > 0 and not r.startswith('-e')
    ]
except:
    INSTALL_REQUIRES = []


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as data:
        return data.read()


if __name__ == '__main__':
    setup(
        name=NAME,
        version=get_version(),
        license=LICENSE,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        url=URL,
        description=DESCRIPTION,
        long_description=read('README.rst'),
        download_url=URL,
        platforms=['any'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Library',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Simplifed BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
        ],
        package_dir={'': 'lib'},
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        scripts=SCRIPTS,
    )
