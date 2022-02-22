import os

# a simple spell to recursively find files with certain extensions
class Accio:
    def __init__(self):
        self.ignored = ""
        self.file_ending = ".intent"

    data = []

    def set_objective(self,objective):
        self.file_ending = objective

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