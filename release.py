#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright 2015 Umbrella Tech.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import os


parser = argparse.ArgumentParser(description='release project')
parser.add_argument('version')
args = parser.parse_args()

with open('setup.py', 'w') as f:
    f.write("""# -*- coding: utf-8 -*-
from distutils.core import setup

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'

setup(
    name='fwf',
    packages=['fwf',],
    version='%s',
    download_url='https://github.com/kelsoncm/fwf/releases/tag/%s',
    description='Python library to manipulate fixed width file',
    long_description=open('README.md', 'rt').read(),
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@gmail.com',
    url='https://github.com/kelsoncm/fwf',
    keywords=['python', 'file', 'fixed', 'width', ],
    classifiers=[]
)
""" % (args.version, args.version,))

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'

os.system("git add setup.py")
os.system("git commit -m 'Release %s'" % args.version)
os.system("git tag %s" % args.version)
os.system("git push --tags origin master")
os.system("python setup.py sdist")
os.system("twine upload dist/fwf-%s.tar.gz" % args.version)
