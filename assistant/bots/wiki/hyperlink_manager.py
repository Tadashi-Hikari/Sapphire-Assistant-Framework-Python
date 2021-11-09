import configparser as cp
import orgparse as org
import re, os, fileinput

config_file = "settings.conf"
# Wiki location/start page
homepage="home.org"
directory_start = "/home/chris/Lab"

# I want it to match existing hyperlinks in org files
note_regex = "\[{2}\S+[(\]{2})|(\]\[\.+\]{2})]..*"
checked_files = [""]

# I need functionality to monitor if those files are renamed, so that wiki-bot can go in and auto update those links
# This may involve needing to know how a system tracks/registers those changes
def find_corresponding_files():
    # I can just search through checked files for the corresponding
    checked_files

# Woo! I got the recursion down good!
def check_directory(directory):
    # Start looking for subdirectories
    listed = os.listdir(directory)
    for path in listed:
        if (os.path.isfile(directory + "/" + path)):
            check_file(directory + "/" + path)
        elif (os.path.isdir(directory + "/" + path)):
            check_directory(directory + "/" + path)


def check_file(path):
    if (checked_files.__contains__(path)):
        return
    else:
        checked_files.append(path)
        check_for_tags(path)


# This needs to be expanded to work w/ arbitrary tags
def check_for_tags(filename):
    regex = re.compile(note_regex)
    # I don't think I need to name it file, but w/e
    file = fileinput.input(filename)
    # I am sure there is an easier way to do this
    if ((filename.endswith("org"))):
        for line in file:
            match_object = regex.search(line)
            if (match_object == None):
                continue
            else:
                # This is just to see if it works, for now
                print("Match found in file ", filename)
                # Group will put it out, rather than string
                print(match_object.group())

if __name__ == '__main__':
    print("Starting wiki bot")
    check_directory(directory_start)

