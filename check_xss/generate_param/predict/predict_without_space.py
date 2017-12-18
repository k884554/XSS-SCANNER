from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.models import model_from_json
from keras.utils import np_utils
import tensorflow as tf
import numpy as np
import random
import sys
import re

class predict_wos:
    def __init__(self, str_seed):
        self.str_seed = str_seed
    
    def predict(self):
        def build_dataset(txt):
                new_word_id = 0
                d_words = []
                t_words = []
                text = txt

                text = text.lower().replace("\n", ",")
                text = re.sub(r'data-.+?=""', "", text)
                text = re.sub(r'=', '=,', text)
                text = re.sub(r'"', ',",', text)
                text = re.sub(r'><', ',>,<', text)
                text = re.sub(r'/>', ',/>,', text)
                text = re.sub(r',,+', ',', text)
                text = re.sub(r'\s\s+', ' ', text)
                text = re.sub(r'\s', ',', text)
                text = re.sub(r',,+', ',', text)
                text = re.sub(r'<wbr,/>,','<wbr,/>', text)

                for word in text.split(","):
                    if word not in d_words:
                        d_words.append(word)
                    t_words.append(word)

                #print("# of distinct words:", len(d_words))
                #print("# of total words:", len(t_words))

                return d_words, t_words

        path = "./corpus/tag_list.txt"
        maxlen = 20

        text = open(path).read().lower()
        d_words, t_words = build_dataset(text)
        d_words = sorted(list(set(d_words)))
        
        word_indices = dict((w, i) for i, w in enumerate(d_words))
        indices_word = dict((i, w) for i, w in enumerate(d_words))
        
        model = model_from_json(open('/Users/NAGAO/antixss/prototype/model/without_space/html_tag_hokan.json').read())
        model.load_weights('/Users/NAGAO/antixss/prototype/model/without_space/html_tag_hokan_weights.h5')

        #model.summary()

        model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

        #buld_seed
        lst = self.str_seed.split(",")
        s = np.zeros((maxlen, len(d_words)), dtype=np.bool)
        l = []
        print(lst)

        for i, word in enumerate(lst):
            if i >= maxlen:
                break
            l.append(word)

        def sample(preds, temperature=1.0):
            # helper function to sample an index from a probability array
            preds = np.asarray(preds).astype('float64')
            preds = np.log(preds) / temperature
            exp_preds = np.exp(preds)
            preds = exp_preds / np.sum(exp_preds)
            probas = np.random.multinomial(1, preds, 1)
            return np.argmax(probas)

        #next_word

        generated = ''
        sentence = l
        for w in sentence:
            generated += w
            
        for w in sentence:
            print(w, end="")
        print('"')
        
        output = ""
        
        for i in range(100):
            x_pred = np.zeros((1, maxlen, len(d_words)))
            for t, word in enumerate(sentence):
                x_pred[0, t, word_indices[word]] = 1

            preds = model.predict(x_pred, verbose=0)[0]

            next_index = np.argmax(preds)
            #next_index = sample(preds, 1.0)
            next_word = indices_word[next_index]

            output += next_word
            sentence.append(next_word)
            sentence = sentence[1:]

            if re.match(r'/*>|</.+?>',next_word):
                break

            sys.stdout.flush()
        
        return output
        