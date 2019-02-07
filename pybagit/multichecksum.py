#!/usr/bin/env python

__author__ = "Andrew Hankinson (andrew.hankinson@mail.mcgill.ca)"
__version__ = "1.5"
__date__ = "2011"
__copyright__ = "Creative Commons Attribution"
__license__ = """The MIT License

                Permission is hereby granted, free of charge, to any person obtaining a copy
                of this software and associated documentation files (the "Software"), to deal
                in the Software without restriction, including without limitation the rights
                to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                copies of the Software, and to permit persons to whom the Software is
                furnished to do so, subject to the following conditions:

                The above copyright notice and this permission notice shall be included in
                all copies or substantial portions of the Software.

                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
                THE SOFTWARE."""

import multiprocessing
import argparse
import os
import sys
import hashlib
import codecs
import re
from pybagit.exceptions import *
from functools import reduce

# declare a default hashalgorithm
HASHALG = 'sha1'
ENCODING = "utf-8"

def write_manifest(datadir, encoding, update=False):
    bag_root = os.path.split(os.path.abspath(datadir))[0]
    manifest_file = os.path.join(bag_root, "manifest-{0}.txt".format(HASHALG))

    checksums = dict()
    files_to_checksum = set(dirwalk(datadir))
    if update and os.path.isfile(manifest_file):
        for line in codecs.open(manifest_file, 'rb', encoding):
            checksum, file_ = line.strip().split(' ', 1)
            full_file = os.path.join(bag_root, file_)
            if full_file in files_to_checksum:
                files_to_checksum.remove(full_file)
                checksums[os.path.join(bag_root, file_)] = checksum

    p = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    result = p.map_async(csumfile, files_to_checksum)
    checksums.update((k, v) for v, k in result.get())
    p.close()
    p.join()

    mfile = codecs.open(manifest_file, 'wb', encoding)

    for file_, checksum in sorted(checksums.items()):
        rp = os.path.relpath(file_, bag_root)
        fl = ensure_unix_pathname(rp)
        mfile.write("{0} {1}\n".format(checksum, fl))

    mfile.close()


def dirwalk(datadir):
    datafiles = []

    for dirpath, dirnames, filenames in os.walk("{0}".format(datadir)):
        for fn in filenames:
            datafiles.append(os.path.join(dirpath, fn))
    return datafiles


def csumfile(filename):
    """ Based on
        http://abstracthack.wordpress.com/2007/10/19/calculating-md5-checksum/
    """
    hashalg = getattr(hashlib, HASHALG)()  # == 'hashlib.md5' or 'hashlib.sha1'
    blocksize = 0x10000

    def __upd(m, data):
        m.update(data)
        return m

    fd = open(filename, 'rb')

    try:
        contents = iter(lambda: fd.read(blocksize), "")
        m = reduce(__upd, contents, hashalg)
    finally:
        fd.close()

    return (m.hexdigest(), filename)


def ensure_unix_pathname(pathname):
    # it's only windows we have to worry about
    if sys.platform != "win32":
        return pathname
    replace = re.compile(r"\\", re.UNICODE)
    fnm = re.sub(replace, "/", pathname)
    return fnm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", help="checksum algorithm to use (sha1|md5)", type=str )
    parser.add_argument("-c", "--encoding", help="File encoding to write manifest", type=str )
    parser.add_argument("-d", "--data_dir", help="Folder where resides files to checksum", type=str)
    parser.add_argument("--update", help="Only update new/removed files", action="store_true" )
    args = parser.parse_args()

    write_manifest(args.data_dir, args.encoding, args.update)
