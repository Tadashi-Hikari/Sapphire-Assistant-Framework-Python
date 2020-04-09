from keras.models import Sequential
from keras.layers import Dense, Activation
import sys, re, pathlib
#from selflib import *

directory = "/home/chris/Lab/assistant/assistant/neural-networks/"

def load_config():
    print("read_config() not yet implemented")
# this is central to the program, so lets just put it up top
def parse(vec): # this is more of a pipeline thing, than a simple act
    models =load_models()
    #if new_models == true:
    #  train_new_models()
    for model in models:
        start.thread(eval(model,vec))
    wait_for_responses()
    pick_highest_conf() #sorting algorithm

# Keras load. taking it down the parse functions
# this was load model, but I have multiple. networks makes more sense
def load_networks(filepath):
    p = pathlib.Path(filepath)
    for i, model in enumerate(p.iterdir()):
        #if the file ends with .nn
        if re.match(".nn$",model):
            networks[i] = keras.models.load_model(filepath)

def train_new_model():
    train()

def get_intents():
    intents = []
    
    directory = "intents"
    path = pathlib.path(directory)
    for intent in path.interdir():
        # I think there is a way to do this with purepath
        if re.match("\.intent$", intent):
            name = pathlib.pureposixpath(intent).name
            intents.append(intent)

    return intents()

def load_sents(filename):
    sents = []
    
    f = open(filename, 'r')
    for line in f:
        sents.append(line)

    return sents

# This is a clusterfuck, and maybe I should have left it as an object
def adjust_for_entities():
    without_entities = sent
    for i, token in enumerate(without_entities):
        if token.startswith('{'):
            # if theres an entity, mark it with a null
            without_entities[i] = ':null:'
    if without_entities != sent:
        return (without_entities, 0.0)
    return None

def train_models():
    #get the number of commands/intents from the database

    train_sents = [()]
    good_match = 1.0
    
    intents = get_intents()

    # a NN for each intent. EVERY INTENT, NOT EVERY SKILL gets an intent
    for intent in intents():
        sent = load_sents(intent)
        #everything below may need to be indented... although this is where padatious runs multi-threads
        train_sents.append((sent,good_match))
        # Weight has to be wors, since weight checks fr entities and such
        weight(sent) # weight is defined below. this is designed for an object... how can I attach it to a non, object?
        train_sents.append(adjust_for_entity)

        #Ah, I need to add in pollute
        pollute() #pollute labes with maybe_match, whicg equals the lenience variable value

        # I think other sents may be other entences from other intents, which would mean theres a lot more bad data than good. I suppose this 'famine' could strenthen the identifiers for the good. See simple_intent.py for more information
        for sent in train_data.other_sents(self.name):

        #do I need to add weights for this sent?
        #what to do with the weights
        #as long as input and output are kept togethe, their indexs will always match. I don't like this though. seems fragile
        vec = vectorize(intent)
        input.append(vec)
        output.append(good_match)
        # the function isn't built for this
        input.append(adjust_for_entity())
        bad_match = 0
        output.append(bad_match)
        

    # This is after that whole for loop
    # inputs are the vectored sentences    
    inputs, outputs = resolve_conflicts(inputs, outputs) # unsure what this does. I think it reates to duplicates. it makes more sense if other_sents are from other intents. it couls be for intents that have near/identical sentences

    #train_data = fann.training_data() # this line needs to be changed. I'm not using fann
    #train_data.set_train_data(inputs,outputs)
    for _ in range(10):
        model.fit(inputs, outputs, 0, 1000, 0, val=loss))
        if callback is optimized:
            break

    save_model(model, name)


    # this needs to be converted to keras. it is trying them until there is decent convergence/optimized loss
    for _ in range(10):
        self.configure_net() # <- I think this is the "compile" in keras
        self.net.train_on_data(train_data, 1000, 0, 0)# fann specific. 1000 epocs
        # is he really testing o his training set? I thought this was bad practice
        #self.net.test_data(train_data)
        #if self.net.get_bit_fail() == 0: # It can stop training when there are no fail bits
            #break

# I actually don't think I need this function if I am not trating it as an object
# add the vector and label
def add(vec, out):
    inputs.append(vectorize(vec)) # what is happening here? add the vector but vectorized?
    outputs.append([out]) #hmm. I thnk out is the label


def weight(sent): # I think this sets the weights for the network.
    def calc_weight(w): #length of the word, raised to the 3rd power... couldn't this just be a random weight?
        return pow(len(w), 3.0)
    total_weight = 0.0
    for word in sent:
        total_weight += calc_weight(word)
    for word in sent: # This is two separate for loops, so that the total_weight is calculated before doing the rest of this
        weight = 0 if word.startswith('{') else calc_weight(word)
        add([word], weight/total_weight) # each word is a portion of the total weight. larger words hold more weight I suppose
    
# test intent. this is just a copy of the test
def setup():
    data.add_lines('bye', ['goodbye', 'bye', 'bye {person}', 'see you later'])
    i_bye = intent('hi') # intent container
    i_bye.train(self.data) # train the individual NN w/ the marked data
    # looks like I need an intent factory

def load_from_database():
    command = ["-t", command_table, "-l"]
    print("calling database")
    data = call_database(command)
    records = deserialize(data)
    
    command = ["-t", training_utterances_table, "-l"]
    data = call_database(command)
    utterances = data.decode('utf-8')
    utterances = utterances.strip()
    utterances = deserialize(utterances)
    notify(utterances) 
    
    for record in records:
        record["utterances"] = []
        for i,utterance in enumerate(utterances):
            if utterance["command"] == record["alias"]:
                record["utterances"].append(utterance["tagged"])

        loud_notify("RECORD",record)
        container.add_intent(record["command"], record["utterances"], True) # this needs to be changed for keras
        # I need to replace this with an intent factory, that holds them all. A linked list should be fine. What about variability of sentence length
    container.train() # this needs to be changed for keras

# Keras save
def save_model():
    filepath = "/dev/null"
    model.save(filepath)
    
# Ah, this is how tests are written...
def test_match():
    assert i_bye.match(['bye']).conf > i_hi.match(['bye']) # trigger if the condition is false. test that it matches properly
    
def match(sent): #slightly modified by me, to remove the object structure
    #return max(0, net.run(vectorize(sent))[0]) #this is the main part of matching intents that needs to be changed to keras
    return predict(sent)

def add_intent(vec):
    inputs.append(vectorize(vec))
    outputs.append([out])

def deterimine_entitky_boundaries():
    print("Not yet implemented")
    # this is entity_edge.py
    # for now, maybe just remove the {}, replace them with :key: or some generic wildcard?

# this was an object. I want to convert it to a dictionary or liked list. is this prudent.
ids = {}
ids['unknown_tokens'] = ':0'
ids['w_1'] = ':1'
ids['w_2'] = ':2'
ids['w_3'] = ':3'
ids['w_4'] = ':4'

def lines_hash():
    # the purpose of this is to see if an intent needs to be retrained
    print("work in progress")

def get_intent():
    # load an intent file from a directory
    print("Work in progress")

def get_entity():    # load the entities
    print("Work in progress")
    
def get_end(sent):
    return len(sent) if self.dir > 0 else -1 # what the fuck?
    
def vector(ids): # I think the # of ids are the num of id'd tokens. It would grow as num of new sentences with unique words are added
    return [0.0] * len(ids) # return a list the size of the ids, as a float list

def vectorize(sent): #vectorize a sentence
    vector = vector(ids)
    unknown = 0 # number of unknown tokens
    # update token count int sent vector?
    for token in sent:
        if token in self.ids: #if the token is in the ids
            ids.assign(vector, token, 1.0) # this is a class thing. I need to change this.
        else:
            unknown += 1

    if len(sent) > 0: # assign the lengths, varied lengths, and unk token number as features to the vector. looks like its a bag of words model?
        ids.assign(vector, ids.unkown, unknown/float(len(sent)))
        ids.assign(vector, ids.w_1, len(sent)/1)
        ids.assign(vector, ids.w_2, len(sent)/2)
        ids.assign(vector, ids.w_3, len(sent)/3)
        ids.assign(vector, ids.w_4, len(sent)/4)

#pollute is adding 
def pollute():
    #I believe p is _ defined as an input?
    def pollute(sent, p):
        sent = sent[:]#this copies to protect the array
        for _ in range(int((len(sent) + 2) / 3)): #for a number of words, based on the length of the sentence plus 2, devided by 3 (probably so it is always >=1)
            sent.insert(p, ':null:')#insert pollution word, equal to null...)
            add(sent, self.LENIENCE) # give it the lenience score

def set_up_model():
    model = Sqeuential() # input layer is one-hot encoded, based on size of sentence, per intent.
    model.add(Dense(10)) # a hidden layer
    model.add(output(1)) # an output layer
    es = EarlyStopping(monitor='val_loss', mode='min', baseline=0.4) # Keras version. this incorporates the set_bit_fail_limit below
    #net.set_bit_fail_limit(0.1) 
    # I think I can replace this with a reasonably optimized loss
    # this is generic from the website
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    #this trains the model
    cb = [es] #callbacks have to be a list
    #model.fit(x_train, y_train, batch_size=128, epochs=20, verbose=0, callbacks=[])
    model.fit(train_features, train_labels, batch_size=128, epochs=20, verbose=0, callbacks=cb)

if __name__ == '__main__':
    
    load_config()
    load_networks(directory) #load known NNs

    train_models() # if there are any hash changes. this is actually handled in parse
        
    user = sys.argv[1:]
    tokens = clean_and_tokenize(user)
    vec = vectorize_features(tokens)
    parse(vec)
    match(vec) # this is where (in intents) padatious matches intents. It needs to get converted over to Keras
