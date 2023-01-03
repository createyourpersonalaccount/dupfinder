# dupfinder

## Description

Dupfinder can help you find duplicate files in your directories. It is
meant to be piped `find` output.

For example:

    # Find duplicate files under my_dir
    find my_dir -type f -print0 | dupfinder

The file names must be separated by NUL bytes, which is why we pass
the `-print0` option to `find`. 

The program **may report** distinct files as duplicates. It is up to
the user to verify the output of the program. In particular, only the
initial 4 MiB are SHA256-hashed; this design choice makes it fast.

Piping the output of `find` offers a certain versatility: multiple
directories can be searched and one can filter for the desired unique
or duplicate items via `grep` or similar.

Files that are unique are printed as

    b'path/file'

while duplicate files are printed as

    [b'path1/file1', b'path2/file2', ...]

Non-printable bytes in the file path are printed using the hexademical
representation as `\xhh`.

There is no particular effort put into this program; it is a simple
program that got the job done.

## Installation

A single console script named `dupfinder` is provided; install with
pip, for example, while at the project root directory:

    pip install .

and uninstall with

    pip uninstall dupfinder

## Examples

1. Search two directories for duplicate PDF files. Lists both
   duplicate and unique files.

        find dir1 dir2 -type f -name '*pdf' -print0 | dupfinder

2. Show only duplicate files under the current directory.

        find . -type f -print0 | dupfinder | grep -v ^b

3. Show only unique files from `dir2`.

        find dir1 dir2 -type f -print0 | dupfinder | grep "^b'dir2/"

4. Grepping for certain paths may be the particular filter you're
   looking for, if the above examples do not suffice.
