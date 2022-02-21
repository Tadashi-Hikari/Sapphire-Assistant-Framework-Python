import sys, nltk
from nltk import word_tokenize
from library.spells import SimpleSpirit

def train():
    # this applies when I am searching for the skill directories
    # intents should be a list of paths
    spirit = SimpleSpirit()
    intents = spirit.search_directory(directory="./skills/")
    
    featuresets = []
    for intent in intents:
        file = open(intent,'r')

        # This is simply predefined for me right now
        word_feature = ["alarm", "set", "weather", "outside"]

        for line in file:
            # I want this tp reset for every line
            features = {}
            tokens = word_tokenize(line)
            for word in word_feature:
                features['contains({})'.format(word)] = (word in tokens)

            # This is a list of feature lists and their corresponding label
            featuresets.append((features,intent))

    # train and return using those features, from the alarm & weather skills
    return nltk.classify.NaiveBayesClassifier.train(featuresets)

if __name__ == "__main__":
    # read the data from stdin
    data = " ".join(sys.argv[1:])
    #print("Received:",data)
    # The words that are relevant to whatever. From EVERYTHING
    word_feature = ["alarm", "set", "weather", "outside"]
    tokens = word_tokenize(data)
    token_set = set(tokens)

    features = {}
    # This is a 'document' level classification. Checking if/what words occur in a string/document
    for word in word_feature:
        features['contains({})'.format(word)] = (word in tokens)

    classifier = train()
    print(classifier.classify(features))
