# dupfinder, find duplicate files.
# Copyright (C) 2023  Nikolaos Chatzikonstantinou
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from hashlib import sha256
from os.path import getsize
from sys import stdin

def main():
    """
    Entry point for dupfinder.
    """

    chunkSize = 4 * 1024 * 1024 # 4 MiB

    # Read a NUL-separated list of files from stdin
    files = stdin.buffer.read().split(b'\x00')
    files = filter(None, files)

    # An association list:
    # the KEY is the file size in bytes
    # the VALUE a list of files with same size
    tmp = {}

    for f in files:
        size = getsize(f)
        try:
            tmp[size].append(f)
        except KeyError:
            tmp[size] = [f]

    # An association list:
    # the KEY is the hash
    # the VALUE a list of "duplicate" files
    duplicates = {}

    # A list of unique files
    uniques = []

    for files in tmp.values():
        if len(files) == 1:
            uniques.append(files[0])
        else:
            for f in files:
                with open(f, mode='rb') as handle:
                    contents = handle.read(chunkSize)
                    h = sha256(contents).digest()
                    try:
                        duplicates[h].append(f)
                    except KeyError:
                        duplicates[h] = [f]

    for f in uniques:
        print(f)

    for files in duplicates.values():
        if len(files) == 1:
            print(files[0])
        else:
            print(files)

    return
