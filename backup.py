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
    parser = argparse.ArgumentParser(usage=("%(prog)s [--exclude|-e excludefile] directory"))
    parser.add_argument("directory",
        type=unicode,
        help="directory to backup")

    parser.add_argument("--exclude","-e",
        dest="exclude",
        type=unicode,
        help="File with the paths to exclude from backup")

    options, args = parser.parse_known_args(argv)

    if not os.path.isdir(options.directory):
        parser.error("Directory not found: '{0}'".format(options.directory))

    if options.exclude:
        with open(options.exclude,'r') as f:
            global excludes
            # Don't use readlines because it keep the newline and pattern will not match
            # excludes = f.readlines()
            excludes = f.read().splitlines()

    if options.directory:
        backup(options.directory)

def backup(path):
    basename = os.path.basename(os.path.normpath(path))
    ext = ".tar.gz"
    tarball = basename + time.strftime("%Y%m%d") + ext

    if os.path.isfile(tarball):
        print "ERROR: Backup file " + tarball + " exits! Abort."
        return

    print "Backup directory " + path + " in tarball " + tarball + " ..."

    with tarfile.open(tarball, "w:gz") as tar:
        if len(excludes) > 0:
            print 'create tarball with exlude option'
            tar.add(path, filter=filter_function)
        else:
            tar.add(path)

    #gpg --symmetric --cipher-algo AES256 filename.tar.gz
    # call(["gpg","--symmetric","--cipher-algo","AES256",fname])

    # move the backup file to the current directory
    # shtil.move(tarball,os.getcwd())

def filter_function(tarinfo):
    for pattern in excludes:
        if fnmatch.fnmatchcase(tarinfo.name,pattern):
            print 'Exclude file {0} pattern({1})'.format(tarinfo.name,pattern)
            return None
    return tarinfo

# Main
if __name__ == "__main__":
        sys.exit(main())
