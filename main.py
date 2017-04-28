"""
Title: Directory Monitor
Author: Darius Strasel
Objective:

- Detect new files in the directory or any subdirectories recursively
- If the file size hasn't changed in >5 seconds, move it to a second directory
- Should handle files that disappear on their own
- For bonus points, be able to scan for new files and handle moving multiple files simultaneously

Constraints:

Accepts two arguments, the directory to watch, and the destination directory for "finished" files.

TODO: Add to function exit_scan() to account for looping. For example, if looping, exit() should not be invoked
or the scan will prematurely cancel as soon as the directory is empty. (Current behavior)

"""
from models import Scan
import argparse
import os


def argument_directory_paths_exists(*input_path):
    """Check if arguments passed thru CLI actually exist."""
    for directory_path in input_path[0]:
        directory = str(directory_path)
        try:
            if os.path.isdir(directory):
                # Then the file exists
                pass
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print("Directory not found: '%s'" % (directory))
            return False
    return True


def return_input_arguments():
    parser = argparse.ArgumentParser(prog='main.py', description='Accept input directories for path monitoring.')
    parser.add_argument('source_directory', metavar='source-path', type=str,
                        help='a directory path representing the source directory.')
    parser.add_argument('target_directory', metavar='target-path', type=str,
                        help='a directory path representing the target directory.')
    args = vars(parser.parse_args())
    return args


def main():
    input_arguments = return_input_arguments()
    source_directory = input_arguments['source_directory']
    target_directory = input_arguments['target_directory']
    if argument_directory_paths_exists([source_directory, target_directory]):
        print("Watching '%s' and sending inputs to '%s'" % (source_directory, target_directory))
        return Scan(source_directory, target_directory)


if __name__ == "__main__":
    main()
