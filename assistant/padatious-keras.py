# Key: search for quick ref
#
# global: definition of a global variable
# pseudocode: needs to be implemented
# verify: suspicious code. may not work. investigate further
# next-steps: code that needs to be implemented, but wont hold up algorithm operation
#
# See relavent notes in the spellbook

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import layers
import tensorflow as tf
import numpy as np
import sys, re, pathlib, keras
from pathlib import Path

# next-steps
def deterimine_entity_boundaries():
    print("Not yet implemented")

def get_sents(path_dir):
    sents = []
    
    path = Path(path_dir)
    for filename in path.iterdir():
        f = open(filename,'r')
        for line in f:
            sents.append((line,filename.name))

    # return a list of tuples
    return sents
    
# ------------------------------------
home = "/home/chris/"
network_dir = home+"Lab/assistant/assistant/neural-networks/"
intent_dir = home+"Lab/assistant/assistant/intents"

# Global to all subfuncs. load sents from all intents.  a list of tuples
ALL_SENTS = get_sents(intent_dir)
LENIENCE = 0.6
GOOD = 1.0

# taken straight from padatious
def tokenize(sentence):
    """
    Converts a single sentence into a list of individual significant units
    Args:
        sentence (str): Input string ie. 'This is a sentence.'
    Returns:
        list<str>: List of tokens ie. ['this', 'is', 'a', 'sentence']
    """
    tokens = []

    class Vars:
        start_pos = -1
        last_type = 'o'

    def update(c, i):
        if c.isalpha() or c in '-{}':
            t = 'a'
        elif c.isdigit() or c == '#':
            t = 'n'
        elif c.isspace():
            t = 's'
        else:
            t = 'o'

        if t != Vars.last_type or t == 'o':
            if Vars.start_pos >= 0:
                token = sentence[Vars.start_pos:i].lower()
                if token not in '.!?':
                    tokens.append(token)
            Vars.start_pos = -1 if t == 's' else i
        Vars.last_type = t

    for i, char in enumerate(sentence):
        update(char, i)
    update(' ', len(sentence))
    return tokens

# next-steps
def check_for_changes():
    return True

def load_config():
    print("Load configis not yet defined")

def adj_token(token):
    # only adjust if its a digit
    if token.isdigit():
        for i in range(10):
            if str(i) in token:
                token = token.replace(str(i), '#')
                #if its the num 0-9, replace w/#
    return token    

#next-steps
def save_ids(ids):
    print("save_ids is not yet defined")

# next-steps. allow for save and recall
def generate_ids(allSents):
    # generic id tokens? verify
    ids = {}
    ids['unknown_tokens'] = 0 #':0'
    ids['w_1'] = 1 #':1'
    ids['w_2'] = 2 #':2'
    ids['w_3'] = 3 #':3'
    ids['w_4'] = 4 #':4'

    for sent,intent in allSents:
        tokens = tokenize(sent)
        for token in tokens:
            token = adj_token(token)
            if token not in ids:
                ids[token] = len(ids) # the value of all ids is its length? This assigns it a unique id, that is the length of the ids at the current moment. If the id doesn't exist, it adds it to the end, gives it the ending number, then increments

    #print all 
    IDS = ids #'unknown_tokens' should be added, at index 0
    return ids

# IDS is implemented here, since python is dynamically typed. it is the id dictionary. this is just floating out here. verify
def get_ids():
    if check_for_changes() == True:
        ids = generate_ids(ALL_SENTS)
        # next-steps. allow for save
        save_ids(ids)
    else:
        ids = load_ids()

    return ids

# Global
IDS = get_ids()

def load_models():
    # there are no models to load
    # if models exist:
    models = gen_all_networks()
    return models
    
# This will need to be threaded.
def gen_all_networks():
    intents = get_intents()

    models = []
    
    for intent in intents:
        models.append(gen_network(intent))
    return models
        
def gen_network(intent):
    # this is where train is getting called 
    model = train(intent)
    return model

# this is done for each network
def train(current):
    # prep the training data
    
    input = []
    output = []
    train_data = [] # should be a list of tuples

    # mark the good sents for this net
    for sent,intent in ALL_SENTS:
        sent = sent.strip()
        # if it doesn't match, skip it
        if (intent != current):
            continue
        train_data.append(add(sent, GOOD))
        tup = ()
        tup = weight(sent) # I don't know if weight is generating properly
        for token,wt in tup:
            train_data.append(add(token,wt)) # what is happening here? it is a vector with a single word, weighted. I believe it is used to determine the importance of that word. I think its conflicts are resolved later with resolve_conflicts, so that the network only trains on a word once, based on its  highest weight

        # pollute the good data. returns tuple
        tokens = tokenize(sent)
        
        # if a word doesn't start with : or is not :?
        if not any(word[0] == ':' and word != ':' for word in tokens):
            out = pollute(sent, 0)
            for sent,label in out:
                train_data.append(add(sent,label))
            
            out = pollute(sent, len(sent))
            for sent,label in out:
                train_data.append(add(sent,label))

    # mark other intents as wrong for this net
    for sent,tent in ALL_SENTS:
        # if it matchs, skip it
        if tent == intent:
            continue  
        train_data.append(add(sent, 0.0)) #how this work now? changed from sent[0]
        #verify, I am starting suspect this only needs to be entered once? maybe not, if we're trying to really reinforce a fail on off sents
        train_data.append(add(':null:', 0.0)) # I think this should only get pulled in if there is a sent that has variables
        train_data.append(add("", 0.0)) # I think this is the None. Verify
    # mark similar sents without entities as wrong.
    for sent,tent in ALL_SENTS:
        # if it doesn't match, skip it
        if tent != intent:
            continue
        without_entities = sent
        for i, token in enumerate(without_entities):
            #if it starts with edge tag
            if token.startswith('{'):
                # replace that word with mull...
                without_entities[i] = ':null:'
        
        if sent != without_entities:
            train_data.append(add(without_entities, 0.0))

    #train_data = resolve_conflicts(train_data)

    # next-steps
    i = 0
    while i < 10:
        # next-steps
        model = build_model(train_data)
        # train if convergence improves
        # i++
        i = 10

    return model

# verify, I think this should work
def parse(input, models):    
    # the input already comes in vectorized
    input = np.array([input])
    
    for model in models:
        predictions = model.predict(input)
        print(predictions)
        
    

# verify. I don't think this code is called  from anywhere
def build_model(train_data):

    train_features = []
    train_labels = []
    
    for data,label in train_data:
        # these are supposed to be vectors, but they're 
        train_features.append(data)
        train_labels.append(label)
    
    model = Sequential(
        [
            layers.Dense(len(IDS)),
            layers.Dense(10),
            layers.Dense(1),
        ]
    )
    es = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', baseline=0.4)
    # this is generic from the website
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    # callback must be a list
    cb = [es]

    #adding numpy here. verify
    train_features = np.array(train_features)
    train_labels = np.array(train_labels)

        # was batch size 128
    model.fit(train_features, train_labels, batch_size=128, epochs=20, verbose=0, callbacks=cb)
    return model

# make a "maybe" sentence
def pollute(sent, p):

    polluted = []
    
    sent = tokenize(sent) #should turn it into a list right?
    for _ in range(int((len(sent) + 2) / 3)): #oh, i don't think this will work. it looks like it's supposed to yeild, not return
        sent.insert(p, ':null:')
        # verify
        newsent = ""
        for token in sent:
            newsent+=" "+token
        polluted.append((newsent.strip(), LENIENCE))
    return polluted

# This is a clusterfuck, and maybe I should have left it as an object. verify
def adjust_for_entities():
    without_entities = sent
    for i, token in enumerate(without_entities):
        if token.startswith('{'):
            # if theres an entity, mark it with a null
            without_entities[i] = ':null:'
    if without_entities != sent:
        return (without_entities, 0.0)
    return None #verify

# this finds the location in the vector and marks it as a val
def assign(vector, key, val):
    # I think vector is representing as a number value
    vector[IDS[adj_token(key)]] = val # <-just set the index
    return vector    
    # vector[id[key]] = val. adj if key is a num. assign the value to the corresponding spot in the vector (bag of words)
        
def vectorize(sent): #vectorize a sentence
    # verify. I think this should be referencing the dict. IDS
    vector = [0.0] * len(IDS)
    unknown = 0

    tokens = tokenize(sent)
    for token in tokens: #this is turning a string into chars
        if token in IDS: #verify. I don't think something is working right here
            vector = assign(vector, token, 1.0)
        else:
            unknown += 1

    # verify. 
    if len(sent) > 0:
        vector = assign(vector, "unknown_tokens", unknown/float(len(sent))) #verify. this works fine. straight from padatious
        vector = assign(vector, "w_1", len(sent)/1)
        vector = assign(vector, "w_2", len(sent)/2)
        vector = assign(vector, "w_3", len(sent)/3)
        vector = assign(vector, "w_4", len(sent)/4)

    return vector
        
# I dont plan in saving just yet. next-steps
def save_model():
    filepath = "/dev/null"
    model.save(filepath) 

def add(vec, out):
    inputs = vectorize(vec) # calling function vectorize
    outputs = [out]

    return (inputs,outputs)

# the dir is a local namespace thing
def get_end(sent):
    return len(sent) if self.dir > 0 else -1 # what the fuck?

# next-steps
def load_config():
    print("read_config() not yet implemented")
    
# I think this way of defining weights preflattens the network
def weight(sent): # I dont see how this is impacting the network. verify
    tokens = tokenize(sent)
    
    temp_train_data = []
    def calc_weight(w):
        return pow(len(w), 3.0)
    total_weight = 0.0
    for token in tokens:
        total_weight += calc_weight(token)
    for token in tokens:
        weight = 0 if token.startswith('{') else calc_weight(token)
        # return wont work, since it outputs multiple. does this need to be a yeild?
        
        temp_train_data.append((token, weight/total_weight))
    return temp_train_data

def load_networks(filepath):
    p = pathlib.Path(filepath)
    for i, model in enumerate(p.iterdir()):
        #if the file ends with .nn
        if re.match(".nn$",model):
            networks[i] = keras.models.load_model(filepath)

# This scrapes the intent directory
def get_intents():
    intents = []
    
    path = pathlib.Path(intent_dir)
    for intent in path.iterdir():
        # I think there is a way to do this with purepath
        name = pathlib.PurePosixPath(intent).name
        if "~" not in name:
            intents.append(name)

    return intents

# taken straight from padatious
def resolve_conflicts(train_data):
    """
    Checks for duplicate sents and if there are any,
    remove one and set the output to the max of the two labels
    Args:
        inputs (list<list<float>>): Array of input vectors
        outputs (list<list<float>>): Array of output vectors
    Returns:
        tuple<inputs, outputs>: The modified inputs and outputs
    """
    inputs = []
    outputs = []

    # whats this doing? see above
    for ins,outs in train_data:
        inputs.append(ins)
        outputs.append(outs)
    
    data = {}
    for inp, out in zip(inputs, outputs):
        tup = tuple(inp)
        if tup in data:
            data[tup].append(out)
        else:
            data[tup] = [out]

    inputs, outputs = [], []
    for inp, outs in data.items():
        inputs.append(list(inp))
        combined = [0] * len(outs[0])
        for i in range(len(combined)):
            combined[i] = max(j[i] for j in outs)
        outputs.append(combined)

    temp_train = ()
    for inp, out in zip(inputs, outputs):
        temp_train.append(inp,out)
    
    return temp_train

# ------------------------------------
if __name__ == '__main__':
    
    load_config()
    load_networks(network_dir) #load known NNs

    # pseudocode
    models = gen_all_networks() # if there are any hash changes. this is actually handled in parse

    # take all command line arguments
    user = sys.argv[1:]
    # next-steps
    #tokens = clean_and_tokenize(user)
    sent = user[0]
    vec = vectorize(sent)
    parse(vec, models) # this is where I inntend to runn the NN itself.
    # match(vec) # this is where (in intents) padatious matches intent
