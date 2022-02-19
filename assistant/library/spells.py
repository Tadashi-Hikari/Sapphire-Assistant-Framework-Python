import os

# Summon a simple spirit to recursively find files with certain extensions
class SimpleSpirit:

    def __init__(self):
        self.ignored = ""
        self.file_ending = ".intent"

    data = []

    # This is designed to be called recursively, to walk a directory looking for valid files
    def search_directory(self,directory):
        contents = os.listdir(directory)
        # Crawl all subsequent paths
        for path in contents:
            absolute = directory+path
            ignore = False

            #ignore those directories
            for item in self.ignored:
                if (absolute.find(item) != -1):
                    #verbose("ignoring directory")
                    ignore = True

            if(ignore == True):
                continue
            elif(os.path.isfile(absolute)):
                # verbose("checking path "+absolute)
                self.check_file(absolute)
            else:
                # verbose("checking path "+absolute)
                self.search_directory(absolute+"/")
        return self.data

    def check_file(self, path):
        if path.endswith(self.file_ending):
            self.data.append(path)