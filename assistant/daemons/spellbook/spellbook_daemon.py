import configparser as cp
import subprocess
import re, os, fileinput
# The goal of this daemon is to... coordinate sub-daemons to manage the spellbook. So... It's kind of like Core for Athena?

config_file = "~/.spellbook"
# Wiki location/start page
homepage="home.org"
directory_start = "/home/chris/Lab/demo-notebook"
notepage="notes.org"
backlink_directory = "/backlink"
backlink_title = "backlink-"
daemon_directory = ""
hub_directory = ""
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
ignored_directories = [directory_start+backlink_directory,directory_start+"/tag-hub"]

# This function reads the command list from the command.conf file
def read_commands():
    file = open(commands,"a+")
    for line in file:
        split = line.split("=")
        # straight forward syntax
        alias = {"":""}
        alias[split[0]] = split[1]

# This function loads all the config file locations, for this specific device
def load_directories():
    home = os.path.expanduser(config_file)
    file = open(home,"r")
    for line in file:
        # all this info is in the config
        info = line.split("=")
        if(info[0] == "root"):
            global directory_start
            directory_start = info[1].strip("\n")
        # right no these append to root, but they should be independant    
        elif(info[0] == "backlink"):
            global backlink_directory
            backlink_directory = info[1]
        elif(info[0] == "hub"):
            global hub_directory
            hub_directory = info[1]
        elif(info[0] == "daemons"):
            global daemon_directory
            daemon_directory = info[1].strip("\n")
        # this last one is asking where the command file is, rather than a directory    
        elif(info[0] == "commands"):
            global command_file
            command_file = info[1]
        file.close()

def check_directory(directory):
    # Start looking for subdirectories
    listed = os.listdir(directory)
    root = directory_start
    for path in listed:
        full = directory+path
        if(os.path.isfile(full)):
            check_file(full)
        elif(os.path.isdir(full)):
            # Ignore the special directories
            if(ignored_directories.__contains__(full)):
                continue
            # Just to keep it from an endless loop. I should incorporate one for tag hubs
            if(full != root+backlink_directory):
                check_directory(full)

# This is checking to make sure the file has the proper endings, and running it through subdaemons
def check_file(path):
    global directory_start
    root = directory_start
    if(checked_files.__contains__(path)):
        return
    else:
        if (path.endswith("md") or (path.endswith("org") or (path.endswith("txt")))):
            # Just pass the file info to the subdaemon. These could be dynamically loaded
            global daemon_directory
            daemons = [daemon_directory+"linker_daemon.py"]
            for daemon in daemons:
                # is there a better way to do this
                subprocess.run(["python3",daemon,"-p",path,"-r",root])

# Should this be moved to a different file
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
        # I need to extract and run the command, that way it's no longer in the note
        return 1

if __name__ == '__main__':
    # This is just so that I see stuff is happening
    print("Starting spellbook bot")
    load_directories()
    check_directory(directory_start)

