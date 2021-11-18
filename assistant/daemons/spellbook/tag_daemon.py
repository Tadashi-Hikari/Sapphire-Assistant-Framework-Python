import argparse
import os

tag_hub_directory="/home/chris/Lab/demo-notebook/tag-hub/"
tag_append = "tag-hub-"
# This file can be queried for tag recommendations
tag_hub_file = "main.org"

def check_for_tags(line,path):
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
                # Call tag_daemon
                command = ["python3", daemon_directory + "/tag_daemon.py", "-t", tag, "-p", path]
                subprocess.run(command)
        return 1

def create_tag_hub_main():
    print("This is a page of all known tags")
    file = open(tag_hub_directory+tag_hub_file,"a+")
    file.close()

def check_tag_hub(tag):
    hub_file = open(tag_hub_directory+tag_hub_file,"a+")
    for line in hub_file:
        if(line == tag):
            hub_file.close()
            return 0
    # since the tag isn't in here, add it. It should link to the localized tag_hub
    hub_file.write("[[./"+tag_append+tag+".org]["+tag+"]]\n")
    hub_file.close()

# This is basically the same as what's above. I feel like I've written this a bunch now
def localized_tag_hub(tag, tagged_file_path):
    local_hub_file = open(tag_hub_directory + tag_append + tag + ".org", "a+")
    for line in local_hub_file:
        if (line == tagged_file_path):
            local_hub_file.close()
            return 0
    local_hub_file.write("[[" + tagged_file_path + "]]\n")
    local_hub_file.close()

# This is causing that loop issue by adding links to the file that is tagging it
def link_tags(tag,tagged_file_path):
    print("linking tags to tag hub")
    # This is for org mode. I could probably make this easier to swap out
    tag_link = "[["+tag_hub_directory+tag_append+tag+".org]["+tag+"]]"
    # This doesn't work because the file is already open, as best I can tell
    tagged_file = open(tagged_file_path,"a+")
    for line in tagged_file:
        # If the link already exists in the file
        print("Comparing",line,"to",tag_link)
        if(line == tag_link):
            tagged_file.close()
            return 0
    tagged_file.write(tag_link+"\n")
    tagged_file.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="simple tag management daemon")
    parser.add_argument('-t', dest='tag', help="tag")
    parser.add_argument('-p', dest='path', help="full path for file that contains tag")
    args = parser.parse_args()

    tag = ""
    path = ""

    if(args.tag is not None):
        print("Tag is",args.tag)
        tag = args.tag
    if(args.path is not None):
        print("Path is",args.path)
        path = args.path

    if(os.path.isdir(tag_hub_directory) == False):
        os.mkdir(tag_hub_directory)
    if(os.path.isfile(tag_hub_directory+tag_hub_file) == False):
        create_tag_hub_main()

    # is this tag in the central hub?
    check_tag_hub(tag)
    # does this tag have its own hub?
    localized_tag_hub(tag,path)
    # Link the tags back to their local hub
    link_tags(tag,path)
