import configparser as cp
import orgparse as org
import re, os, fileinput

config_file = "settings.conf"
# Wiki location/start page
homepage="home.org"
directory_start = "/home/chris/Lab/Notebook "
notepage="notes.org"

# This should pull Note or note
noteRegex = "^[N|n]ote:"
# This just keeps a list of which files have been checked
checkedFiles = [""]

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
    if(checkedFiles.__contains__(path)):
        return
    else:
        checkedFiles.append(path)
        check_for_tags(path)

# This needs to be expanded to work w/ arbitrary tags
def check_for_tags(filename):
    regex = re.compile(noteRegex)
    # I don't think I need to name it file, but w/e
    file = fileinput.input(filename)
    # I am sure there is an easier way to do this
    if(filename.endswith("md") or (filename.endswith("org"))):
        for line in file:
            match_object = regex.match(line)
            if(match_object == None):
                continue
            else:
                # This is just to see if it works, for now
                print("Match found in file ",filename)
                print(match_object.string)

if __name__ == '__main__':
    print("Starting wiki bot")
    check_directory(directory_start)

