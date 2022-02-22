# load list of entities (per skill)
# after classified, manually add entry
# just update the list when you need to. This will at least get it working
from nltk import word_tokenize
from library.spells import Accio
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="main udp server and router")
    parser.add_argument('-u', dest="utterance",nargs="+")
    parser.add_argument('-i', dest="intent")
    args = parser.parse_args()

    utterance = args.utterance

    intent = None
    if(args.intent != None):
        intent = args.intent

    #print(utterance)

    extension = "entity"

    accio = Accio()
    accio.set_objective(extension)
    directories = accio.search_directory(directory="./skills/")

    entities = []
    for filepath in directories:
        file = open(filepath,'r')
        # expecting a single word per line
        for line in file:
            entities.append(line.strip())

    #word_tokens = word_tokenize(utterance)
    word_tokens = utterance
    extracted = []

    for word in word_tokens:
        if word in entities:
                extracted.append(word)

    print(extracted)