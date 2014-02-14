#!/usr/bin/env python
# -*- mode: Python;-*-
# -*- coding: utf-8 -*-
"""
" Copyright (c) 2013 Laurent Zubiaur
"
" http://www.pix2d.com/
"
" Permission is hereby granted, free of charge, to any person obtaining a copy
" of this software and associated documentation files (the "Software"), to deal
" in the Software without restriction, including without limitation the rights
" to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
" copies of the Software, and to permit persons to whom the Software is
" furnished to do so, subject to the following conditions:
" 
" The above copyright notice and this permission notice shall be included in
" all copies or substantial portions of the Software.
" 
" THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
" IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
" FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
" AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
" LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
" OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
" THE SOFTWARE.
"""

import sys, os, time, shutil
from subprocess import call
import tarfile
import argparse
import fnmatch

excludes = None

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser(usage=("%(prog)s [--gpg] [--exclude|-e excludefile] path"))

    parser.add_argument("path",
        type=unicode,
        help="Directory to backup")

    parser.add_argument("--exclude","-e",
        dest="exclude",
        type=unicode,
        help="File with the paths to exclude from backup")

    parser.add_argument("--gpg","-g",
        dest="encrypt",
        action="store_true",
        help="Enable gpg symetric encryption")

    options, args = parser.parse_known_args(argv)

    if not os.path.isdir(options.path):
        parser.error("Directory not found: '{0}'".format(options.path))

    if options.exclude:
        with open(options.exclude,'r') as f:
            global excludes
            # Don't use readlines because it keep the newline and pattern will not match
            # excludes = f.readlines()
            excludes = f.read().splitlines()
    
    # Figure out the tarball filename from the directory name
    basename = os.path.basename(os.path.normpath(options.path))
    tarball = "{0}_{1}.tar.gz".format(basename,time.strftime("%Y%m%d"))

    if os.path.isfile(tarball):
        print "ERROR: Backup file '{0}' exits! Abort.".format(tarball)
        return

    print "Backup directory {0} in tarball {1}...".format(options.path,tarball)

    if options.path:
        backup(options.path,tarball)

    if options.encrypt:
        encrypt(tarball)

def backup(path,tarball):
    with tarfile.open(tarball, "w:gz") as tar:
        if excludes and len(excludes) > 0:
            print 'Create tarball with exlude option'
            tar.add(path, filter=filter_function)
        else:
            tar.add(path)

def encrypt(filename):
    print 'Encrypt tarball using GnuPG'
    call(['gpg2','--symmetric','--cipher-algo','AES256',filename])

def filter_function(tarinfo):
    for pattern in excludes:
        if fnmatch.fnmatchcase(tarinfo.name,pattern):
            print 'Exclude file {0} pattern({1})'.format(tarinfo.name,pattern)
            return None
    return tarinfo

# Main
if __name__ == "__main__":
        sys.exit(main())
