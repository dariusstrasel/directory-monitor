"""

Don't spend more than an hour on this project. Create a Python program from scratch that will watch a directory for files and moves them elsewhere when they are 'done' being written. A successful implementation will be able to:

- Detect new files in the directory or any subdirectories recursively
- If the file size hasn't changed in >5 seconds, move it to a second directory
- Should handle files that disappear on their own
- For bonus points, be able to scan for new files and handle moving multiple files simultaneously

Constraints:

Accepts two arguments, the directory to watch, and the destination directory for "finished" files
Only use libraries built into Python itself (ie. ‘os’, ‘sys’, etc). Nothing from pypi or other external sources.
Use Python 2.7 or 3+.

"""

import os, shutil, time
from sys import argv
from os.path import join


def scan_directory(path):
    # root_list = []
    # dirs_list = []
    file_list = []

    for root, dirs, files in os.walk(path):
        # root_list.append(root)
        # dirs_list.append(dirs)
        for item in files:
            file_list.append(join(root, item))
    return file_list


def file_is_changed_within_5_seconds(source):
    file_info = os.stat(source)
    last_modified = file_info['st_mtime']
    for scan_period in range(0, 4):
        time.sleep(1)
        if last_modified != file_info['st_mtime']:
            return True
    return False


def process_files():
    for file in scan_directory(argv[1]):
        if file_is_changed_within_5_seconds(file):
            move_file(file, argv[2])
        else:
            move_file(file, argv[2])


def move_file(source, destination):
    try:
        shutil.move(source, destination)
    except shutil.Error: # Need to catch "same_file errors"
        pass


def main():
    # scan_directory('..')
    print(argv)
    process_files()


if __name__ == "__main__":
    main()