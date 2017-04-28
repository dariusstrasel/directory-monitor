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
from sys import argv
import os


def argument_is_string(argument):
    try:
        int(argument)
        return False
    except ValueError:
        return True


def time_length_is_valid():
    try:
        if not argument_is_string(argv[3]):
            return True
    except IndexError:
        return False


def input_is_valid(arguments):
    argument_length = len(arguments)
    if argument_length == 4 or argument_length == 3:
        if False in ([argument_is_string(argument) for argument in arguments[:3]]):
            print("Ensure arguments are valid paths. (Cannot be a number.)")
            return False
        if not time_length_is_valid():
            print("Time Length not valid.")
            return False
        else:
            return True
    print("Not enough arguments: %s/%s" % (len(arguments), 3))
    return False


def argument_file_exists(*input_path):
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
    return True


def main():
    parser = argparse.ArgumentParser(prog='main.py', description='Accept input directories for path monitoring.')
    parser.add_argument('string1', metavar='source-path', type=str,
                        help='a file directory representing the source directory.')
    parser.add_argument('string2', metavar='target-path', type=str,
                        help='a file directory representing the target directory.')
    args = vars(parser.parse_args())
    source_directory = args['string1']
    target_directory = args['string2']
    if argument_file_exists([source_directory, target_directory]):
        print(source_directory, target_directory)
    # return Scan(argv[1], argv[2])


if __name__ == "__main__":
    main()
