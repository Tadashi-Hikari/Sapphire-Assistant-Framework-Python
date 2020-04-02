from keras.models import Sequential
from keras.layers import Dense, Activation

# What is the purpose of this "Do one thing well?"
  # Train and parse utterances

# config comes during the setup
def read_config():
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
def load_model():
    filepath = "null"
    keras.models.load_model(filepath)

def train_new_model():
    train()

def train():
    for sent in train_data.my_sents(name):
        add(sent, 1.0) # add the sent, mark it as true, since its explicitly added to trigger the command

        weight(sent) # weight is defined below
        
    for sent in train_data.my_sents(name):
        without_entities = sent
        for i, token in enumerate(without_entities):
            if token.startswith('{'):
                # if theres an entity, mark it with a null
                without_entities[i] = ':null:'
        if without_entities != sent:
            add(without_entities, 0.0)

    inputs, outputs = resolve_conflicts(inputs, outputs) # unsure what this does

    train_data = fann.training_data() # this line needs to be changed. I'm not using fann
    train_data.set_train_data(inputs,outputs)


    # this needs to be converted to keras
    for _ in range(10):
        self.configure_net()
        self.net.train_on_data(train_data, 1000, 0, 0)# fann specific. 1000 epocs
        self.net.test_data(train_data)
        if self.net.get_bit_fail() == 0: # It can stop training when there are no fail bits
            break

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
        weight = 0 if word.startswith('{'} else calc_weight(word)
        add([word], weight/total_weight) # each word is a portion of the total weight. larger words hold more weight I suppose
    
# test intent. this is just a copy of the test
def setup():
    data.add_lines('bye', ['goodbye', 'bye', 'bye {person}', 'see you later'])
    i_bye = intent('hi') # intent container
    i_bye.train(self.data) # train the individual NN w/ the marked data
    # looks like I need an intent factory

# Keras save
def save_model
    filepath = "/dev/null"
    model.save(filepath)
    
# Ah, this is how tests are written...
def test_match):
    assert i_bye.match(['bye']).conf > i_hi.match(['bye']) # trigger if the condition is false. test that it matches properly
    
def match(sent): #slightly modified by me, to remove the object structure
    #return max(0, net.run(vectorize(sent))[0]) #this is the main part of matching intents that needs to be changed to keras
    return predict(sent)

def add_intent(vec):
    inputs.append(vectorize(vec))
    outputs.append([out])

def deterimine_entity_boundaries():
    # this is entity_edge.py
    # for now, maybe just remove the {}, replace them with :key: or some generic wildcard?
    
class ids(StrEnum): # the purpose is to give a unique ID for tokens, from padatious. do I want this?
    unknown_tokens = ':0'
    w_1 = ':1'
    w_2 = ':2'
    w_3 = ':3'
    w_4 = ':4'

''' each token has an id, the id process goes throug the directory and returns the values?, excluding __* adn the value identifier. dir = list of names in current local scope. like a dict for objects. strings as keys. I think each value word is a key. dir = objects __dict__ attribute. object input is IdManager (self). init w/ no ids, unless passed ides.
  -add_token = self.adj_token(token)? and if its not in the id, then it adds it to the id w/ the len of the id? id is dict, token is key, value = len of the id (len of the token string)
--adj_token makes a string a number. must mean adjust token
- calls add_token for each token in an add_sent(sent) '''

def lines_hash():
    # the purpose of this is to see if an intent needs to be retrained
    print("work in progress")

def get_intent():
    # load an intent file from a directory
    print("Work in progress")

def get_entity():
    # load the entities
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
    parser = argparse.ArgumentParser(description="All in one intent parser")
    parser.add_argument('-p', dest='parse', help="enter a textual command (as if spoken)")

    args = parser.parse_args()
    
    load_config()
    load_networks() #load known NNs

    if args.parse is not None:
        check_for_updates() # if there are any hash changes. this is actually handled in parse
        
        user = args.parse
        tokens = clean_and_tokenize(user)
        vec = vectorize_features(tokens)
        parse(vec)
        match(vec) # this is where (in intents) padatious matches intents. It needs to get converted over to Keras

    if args.train == True:
        set_up_model()
        for model in dir:
            train_new_model()

'''
----NOTES-----

# notes on the id class
FROM THE CREATOR:  So, words are converted into indices like  apple -> 2 and orange -> 3

Then, to generate an input vector, if a word in the sentence exists, it's index is set to 1.0. So, the sentence apple orange the vector could be 0 0 1 1. But, we want to add extra info like how many words are in the sentence. To do we map some random identifier like :num_words (the colon in front guarantees it won't collide with a real word someone has in their intent file) to an unused index like 4 and then our final vector might be apple orange -> 0 0 1 1 2. Instead of :num_words I just put :1, :2, :3...

TL;DR, they are random string identifiers that have locations in the vector for extra sentence features.

Oh, I forgot to specifically address that part. So, each w_1 through w_4 is a feature for the length of the sentence divided by 1 through 4. It's probably not useful honestly, but it's in case it helps train.'''
