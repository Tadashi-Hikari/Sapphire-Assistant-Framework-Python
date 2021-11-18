import argparse, re, os

config = "~/.spellbook"

root = ""
backlink_directory = ""
org_link_regex = "\[{2}.+\]{1,2}"

def load_directories():
    file = open(os.path.expanduser(config),"r")
    for line in file:
        info = line.split("=")
        if(info[0] == "backlink"):
            global backlink_directory
            backlink_directory = info[1]
        if(info[0] == "root"):
            global root
            root = info[1]
    file.close()

# Do I def want to generate this header?
def generate_header_links(lines,root):
    header = "==|[["+root+"/tag-hub][Home]]|"
    other_headers = [""]
    for other in other_headers:
        header.concat(other+"|")

    header.concat("==")
    found = False
    # If the header exists, update it
    for index,line in enumerate(lines):
        if((line.startswith("==|")) and (line.endswith("|=="))):
            lines[index] = header
            found = True

    updated_lines = [""]
    if(found == False):
        updated_lines[0] = header
        updated_lines.append(lines)
    else:
        updated_lines = lines

    return updated_lines

def check_for_links(line,path):
    global org_link_regex
    regex = re.compile(org_link_regex)
    match_link = regex.search(line)

    print("checking for links")
    if(match_link == None):
        return 0
    else:
        subregex = "\[{2}\S+?\]{1}"
        match_sub = re.compile(subregex)
        thing = match_sub.search(match_link.group())
        linked_file = thing.group().strip("[").strip("]")
        backlink_prefix="backlink-"
        backlink = backlink_prefix+linked_file
        print("found link. making backlink")
        backlink(path,backlink)
        return 1

def backlink(path,backlink_file):
    global root
    global backlink_directory
    backlink_path = root+backlink_directory+backlink_file
    if (os.path.isdir(directory_start + backlink_directory) == False):
        print("Creating backlink directory")
        os.mkdir(directory_start+backlink_directory)
    file = open(backlink_path,"a+")
    link_path = "[[" + path + "]]"
    for line in backlink_file:
        if(line == link_path):
            print("This backlink exists already")
            file.close()
            return
    print("Adding a new backlink")
    # Make it, ya know, linkable
    file.write("[["+link_path+"]]"+"\n")
    file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="simple tag management daemon")
    parser.add_argument('-r', dest='root', help="what is the root directory for the spellbook")
    parser.add_argument('-p', dest='path', help="full path for file that contains tag")
    args = parser.parse_args()

    root = args.root
    path = args.path

    lines = []
    
    file = open(args.path,"w")
    for line in file:
        check_for_links(line,path)
    file.close()
