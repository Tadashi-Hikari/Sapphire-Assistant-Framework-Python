# The most essential features are:
# Works on Android/Linux
# Linkbacks & homepage
# Tag linking

import re, os

root_directory = ""
hub_directory = ""
backlink_directory = ""
tag_prefix = "tag-hub-"
backlink_prefix = "backlink-"
# I don't think this will update with the variables. I need to be mindful of this
ignored = [""]

def config():
    global root_directory, hub_directory, backlink_directory, ignored
    
    conf = os.path.expanduser("~/.spellbook")
    file = open(conf,"r")
    for line in file:
        info = line.strip("\n").split("=")
        if(info[0] == "root"):
            root_directory = info[1]
        if(info[0] == "hub"):
            hub_directory = info[1]
        if(info[0] == "backlink"):
            backlink_directory = info[1]
    file.close()
    # Update the directories to NOT crawl
    ignored = [hub_directory,backlink_directory]

def crawl_spellbook(directory):
    contents = os.listdir(directory)
    for path in contents:
        absolute = directory+path
        if(os.path.isfile(absolute)):
           check_file(absolute)
        elif(ignored.__contains__(absolute)):
           continue
        else:
           crawl_spellbook(absolute)
           
def check_file(path):
    if(path.endswith("org") or
       path.endswith("md")):
        check_for_links(path)
        check_for_tags(path)

def check_for_links(path):
    global root_directory, backlink_directory, backlink_prefix
    # This is for org mode
    link_regex = "\[{2}.+\]{1,2}"
    filename = "\[{2}\S+?\]{1}"

    if (os.path.isdir(root_directory + backlink_directory) == False):
        os.mkdir(root_directory + backlink_directory)

    regex = re.compile(link_regex)
    subregex = re.compile(filename)
    file = open(path, "a+")

    for line in file:
        match_object = regex.search(line)
        if (match_object == None):
            continue
        else:
            match_sub = re.compile(subregex)
            thing = match_sub.search(match_object.group())
            linked_file = thing.group().strip("[").strip("]")
            backlink_file = backlink_prefix + linked_file
            backlink(path, backlink_file)
    file.close()

# I need to find better names for these things
def backlink(path,backlink_file):
    global root_directory, backlink_directory
    backlink_path = root_directory+backlink_directory+backlink_file

    # This is a different file than the one above. This is the backlink file
    file = open(backlink_path, "a+")
    link_path = "[[" + path + "]]"
    for line in backlink_file:
        if (line == link_path):
            file.close()
            return
    # Make it, ya know, linkable
    file.write("[[" + link_path + "]]" + "\n")
    file.close()

# This is where the header/footer portion should come in. I don't want to constantly make new tag stuff
def check_for_tags(path):
    # This is for org mode
    tag_regex = ":(\S+?:)+"
    regex = re.compile(tag_regex)

    global root_directory, hub_directory
    if (os.path.isdir(root_directory + hub_directory) == False):
        os.mkdir(root_directory + hub_directory)

    file = open(path, "a+")

    for line in file:
        match_object = regex.search(line)
        if (match_object == None):
            continue
        else:
            for tag in match_object.group().split(":"):
                if (tag != ""):
                    check_tag_hub(tag)
                    link_tags(tag,path)
    file.close()

def check_tag_hub(tag):
    global hub_directory, tag_prefix
    hub_file = "tag-hub-main.org"

    # This is a different file than the one above. This is the main tag hub file
    hub_file = open(hub_directory + hub_file, "a+")
    for line in hub_file:
        if (line == tag):
            hub_file.close()
            return 0
    # since the tag isn't in here, add it. It should link to the localized tag_hub
    hub_file.write("[[./" + tag_prefix + tag + ".org][" + tag + "]]\n")
    hub_file.close()

# This creates a link TO the local tag hub in the existing tagged file
def link_tags(tag,tagged_file_path):
    global hub_directory, tag_prefix

    # This is a different file than the one above. This is the local tag hub file
    local_hub_file = open(hub_directory + tag_prefix + tag + ".org", "a+")
    for line in local_hub_file:
        if (line == tagged_file_path):
            local_hub_file.close()
            return 0
    local_hub_file.write("[[" + tagged_file_path + "]]\n")
    local_hub_file.close()

if __name__ == '__main__':
    config()