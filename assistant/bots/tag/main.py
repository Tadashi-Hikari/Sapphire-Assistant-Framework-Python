# this is simply going to make a 'tag'.org based on the tag name. and it will pick up the command syntax

import configparser as cp
import orgparse as org
import re, os, fileinput

config_file = "settings.conf"
# Wiki location/start page
homepage="home.org"
directory_start = "/home/chris/Lab/demo-notebook"
notepage="notes.org"
backlink_directory = "/backlink"
backlink_title = "backlink-"
# This is the original. Why did I make it so long!
# org_link_regex = "\[{2}\S+[(\]{2})|(\]\[\.+\]{2})]..*"
org_link_regex="\[{2}.+\]{1,2}"

# Tags look like :this: or #this. Tags can be :strung:together:like:this:
# commands look like -this- and commands w/ subcommands look -like-+this+
# should they -look+like+this+ instead? (I can drop the trailing - because its followed by a +
command_regex = "-\w+(-{1}|(\+\w+\+*)+-{1})"
org_mode_tag_regex = ":(\S+?:)+"

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
        if (path.endswith("md") or (path.endswith("org") or (path.endswith("txt")))):
            file = fileinput.input(path)
            for line in file:
                # This is just to keep the system from matching commands inside tags and links. idk that I want it to do that
                checked_files.append(path)
                if(check_for_links(line,path)):
                    continue
                if(check_for_tags(line)):
                    continue
                check_for_commands(line)


# This needs to be expanded to work w/ arbitrary tags
def check_for_commands(line):
    # I may want to move this to global, so that it's not a waste of cycles
    regex = re.compile(command_regex)
    # I don't think I need to name it file, but w/e
    # I am sure there is an easier way to do this
    match_object = regex.search(line)
    if(match_object == None):
        return 0
    else:
        # This is just to see if it works, for now
        print("command found")
        print(match_object.group())
        return 1

def check_for_tags(line):
    regex = re.compile(org_mode_tag_regex)
    match_tag = regex.search(line)
    if(match_tag == None):
        return 0
    else:
        print("Tags found")
        print(match_tag.group())
        # No need to regex here
        for tag in match_tag.group().split(":"):
            if(tag != ""):
                print(tag)
        return 1

# I hacked this together. Could probably do it more elegantly
def check_for_links(line,path):
    # I may want to move this to global, so that it's not a waste of cycles
    regex = re.compile(org_link_regex)
    match_link = regex.search(line)
    # This is the regex for links, and I am using it to create the 'backlink' pages
    if(match_link == None):
        return 0
    else:
        print("Link found")
        print(match_link.group())
        # This is lazy, but it works. I could just split it, yeah?
        subregex = "\[{2}\S+?\]{1}"
        match_sub = re.compile(subregex)
        thing = match_sub.search(match_link.group())
        link = thing.group()
        # I will need to do some verification to ensure it's linking to a file
        print("The link should be")
        link = link.strip("[").strip("]")
        print("The full link path is:",backlink_title+link)
        backlink = backlink_title+link
        backlink_link(path,backlink)
        # if currently checked path exists, do nothing
        # if currently checked path doesn't exist in backlink, append
        return 1

def backlink_link(path,backlink_file):
    backlink_path = directory_start+backlink_directory+"/"+backlink_file
    if(os.path.isdir(directory_start+backlink_directory) == False):
        print("Creating backlink directory")
        os.mkdir(directory_start+backlink_directory)
    file = open(backlink_path,'w')
    link_path = "[[" + path + "]]"
    for line in backlink_file:
        # Every line should be EXACTLY the path to a file that links to it (should it incorporate WHERE it's linked? like a subheader # does in HTML)
        if(line == link_path):
            print("This backlink exists already")
            file.close()
            return
    print("Adding a new backlink")
    file.write(link_path)
    file.close()

if __name__ == '__main__':
    print("Starting wiki bot")
    check_directory(directory_start)

