#!/usr/bin/env bash
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

PROJECT_NAME="pyfwf"
FULL_IMAGE_NAME="kelsoncm/$PROJECT_NAME"

if [[ $# -ne 2 ]] || [[ "$1" != "-l" && "$1" != "-p" && "$1" != "-r" && "$1" != "-a" ]]
  then

  if [[ "$#" == 0 ]]
    then
    echo "ERROR: Chooce a option."
  else
    if [[ "$1" != "-l" && "$1" != "-p" && "$1" != "-r" && "$1" != "-a" ]]
      then
      echo "ERROR: Invalid option: $1."
    elif [[ "$#" == 1 ]]
      then
      echo "ERROR: Set a version number."
    fi
  fi

    echo "
NAME
       release
SYNOPSIS
       ./release.sh [-l|-p|-r|-a] <version>
DESCRIPTION
       Create a new release $PROJECT_NAME image.
OPTIONS
       -l         Build only locally
       -p         Push to GitLab
       -r         Registry on GitLab
       -a         Push and registry on GitLab
       <version>  Release version number
EXAMPLES
       o   Build a image to local usage only:
                  ./release.sh -b 1.0
       o   Build and push to GitHub:
                  ./release.sh -p 1.0
       o   Build and registry on GitHub:
                  ./release.sh -r 1.0
       o   Build, push and registry on GitHub:
                  ./release.sh -a 1.0
LAST TAG: $(git tag| tail -1)"
    exit
fi

create_setup_cfg_file() {
    echo """# -*- coding: utf-8 -*-
from distutils.core import setup
__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'
setup(
    name='$PROJECT_NAME',
    packages=['$PROJECT_NAME',],
    version='%s',
    download_url='https://github.com/$FULL_IMAGE_NAME/releases/tag/$1',
    description='Python library to manipulate fixed width file',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@gmail.com',
    url='https://github.com/$FULL_IMAGE_NAME',
    keywords=['python', 'file', 'fixed', 'width', ],
    classifiers=[]
)
""" > setup.py

    echo "Build local version $FULL_IMAGE_NAME $2"
    echo ""
    docker build -t $FULL_IMAGE_NAME:latest --force-rm .
    docker run --rm -it -v `pwd`:/src $FULL_IMAGE_NAME:latest sh -c 'coverage run -m unittest tests/test_* && coverage report -m'

}

create_setup_cfg_file $2

if [[ "$1" == "-p" || "$1" == "-a" ]]
then
  echo ""
  echo "GitHub: Pushing"
  echo ""
  git add setup.py
  git commit -m "Release $2"
  git tag $2
  git push --tags origin master
fi

if [[ "$1" == "-r" || "$1" == "-a" ]]
then
  echo ""
  echo "PyPI Hub: Uploading"
  echo ""
  docker login
  docker run --rm -it -v `pwd`:/src $FULL_IMAGE_NAME:latest twine upload dist/$PROJECT_NAME-$2.tar.gz
fi

echo ""
echo "Done."

echo ""
echo "Done."
