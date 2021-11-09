# this is simply going to make a 'tag'.org based on the tag name. and it will pick up the command syntax

import configparser as cp
import orgparse as org
import re, os, fileinput

config_file = "settings.conf"
# Wiki location/start page
homepage="home.org"
directory_start = "/home/chris/Lab/Notebook "
notepage="notes.org"

# Tags look like :this: or #this. Tags can be :strung:together:like:this:
# commands look like -this- and commands w/ subcommands look -like-+this+
# should they -look+like+this+ instead? (I can drop the trailing - because its followed by a +
command_regex = "-\w+(-{1}|(\+\w+\+*)+-{1})"
org_mode_tag_regex = ":(\S+:)+"

# This simple syntax could be kept, especially if I want to yank a whole line, and I know it beforehand...?
# Am I splitting things up too much?
note_regex = "^[N|n]ote:"
# This just keeps a list of which files have been checked
checked_files = [""]

# inotify can just let this bot know when things have happened

# Woo! I got the recursion down good!
def check_directory(directory):
    # Start looking for subdirectories
    listed = os.listdir(directory)
    for path in listed:
        if(os.path.isfile(directory+"/"+path)):
            check_file(directory+"/"+path)
        elif(os.path.isdir(directory+"/"+path)):
            check_directory(directory+"/"+path)

def check_file(path):
    if(checked_files.__contains__(path)):
        return
    else:
        checked_files.append(path)
        check_for_tags(path)

# This needs to be expanded to work w/ arbitrary tags
def check_for_tags(filename):
    regex = re.compile(command_regex)
    # I don't think I need to name it file, but w/e
    file = fileinput.input(filename)
    # I am sure there is an easier way to do this
    if(filename.endswith("md") or (filename.endswith("org") or (filename.endswith("txt")))):
        for line in file:
            match_object = regex.search(line)
            if(match_object == None):
                continue
            else:
                # This is just to see if it works, for now
                print("Match found in file ",filename)
                print(match_object.group())

if __name__ == '__main__':
    print("Starting wiki bot")
    check_directory(directory_start)

