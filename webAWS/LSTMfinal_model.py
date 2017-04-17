import numpy as np
import re
import nltk
import os
from random import shuffle
from keras.preprocessing.text import one_hot
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.models import model_from_json
from newspaper import Article

class lstm_model:
    def transform_keywords(self, file_name):
        inf_file = open(file_name)
        data = list()
        for one_news in inf_file.readlines():
            single = one_news.strip().split(',')
            mapping = list()
            for one_keyword in single:
                mapping.append(one_hot(one_keyword, 7000)[0])
            data.append(mapping)
        #print(data)
        return data

    def transform_titles(self, file_name):
        inf_file = open(file_name)
        data = list()
        for one_news in inf_file.readlines():
            single = nltk.word_tokenize(self.clean_sentence(one_news))
            mapping = list()
            for one_keyword in single:
                mapping.append(one_hot(one_keyword, 7000)[0])
            data.append(mapping)
        # print(data)
        return data

    def clean_sentence(self,s):
        c = s.lower().strip()
        return re.sub('[^a-z ]', '', c)

    '''
    :param
        type: 0 indicates using the keywords from the content
              1 indicates using the titles
    '''
    def save_model(self, fake_file, real_file, type, model_name, unit_size = 10):
        batch_size = 10
        if type == 0:
            fake_data = self.transform_keywords(fake_file)
            real_data = self.transform_keywords(real_file)
        else:
            fake_data = self.transform_titles(fake_file)
            real_data = self.transform_titles(real_file)
            batch_size = 32
        labels = list()
        max_len = 0
        for i in fake_data:
            labels.append(0)
        for i in real_data:
            labels.append(1)
        data=fake_data
        for r in fake_data:
            if max_len < len(r):
                max_len = len(r)
        for r in real_data:
            if max_len < len(r):
                max_len = len(r)
            data.append(r)
        for d in data:
            cur_len = len(d)
            while cur_len < max_len:
                d.append(0)
                cur_len = cur_len+1

        #shuffle the given data
        index_shuf = list(range(len(data)))
        shuffle(index_shuf)
        data_shuffled = list()
        label_shuffled = list()
        for i in index_shuf:
            data_shuffled.append(data[i])
            label_shuffled.append(labels[i])
        model = Sequential()
        model.add(Embedding(7000, 256, dropout=0.2))
        model.add(LSTM(16, dropout_W=0.2, dropout_U=0.2))  # try using a GRU instead, for fun
        model.add(Dense(1))
        model.add(Activation('sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

        model.fit(data_shuffled, label_shuffled,
                  nb_epoch=10,
                  batch_size=batch_size,
                  shuffle=False)
        # serialize model to JSON
        model_json = model.to_json()
        with open(model_name, "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("model.h5")
        print("Saved model to disk")

    def reload_model(self, file_name, mh5):
        json_file = open(file_name, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")
        return loaded_model

    #max_len for keywords: , max_len_for_titles:
    def format_testcase(self,string, type, max_len):
        #titles
        single = list()
        if type == 0:
            single = nltk.word_tokenize(self.clean_sentence(string))
        #keywords
        else:
            single = string
        mapping = list()
        for one_keyword in single:
            mapping.append(one_hot(one_keyword, 7000)[0])
        while len(mapping) < max_len:
            mapping.append(0)
        data = list()
        data.append(mapping)
        print(data)
        return mapping

if __name__ == "__main__":
    #Task on the content keywords
    #save_model("./fakenews_keywords.csv","./realnews_keywords.csv",0,"model_keywords.json")
    #Task on the titles
    #save_model("./data/titles/fake_news_training.txt", "./data/titles/real_news_training.txt",1,"model_titles.json" )
    #Redload a save model:
    #Extract keywords from the web
    article = Article('https://www.facebook.com')
    article.download()
    article.parse()
    article.nlp()
    print(article.keywords)
    mod = lstm_model()
    model = mod.reload_model('model_titles.json','model.h5')

    '''parse the input from web front end, say the keywords/titles are raw strings
    TODO: 1) Preprocess the string such that only words count
          2) Form the corresponding matrix by calling the function like:
            (max_len is determined by the training model)
            format_testcase(string, type=1 for keywords, 0 for title, max_len = 19 for keywords, =39 for titles):'''


    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    X = mod.format_testcase(article.keywords, 1,19)
    result = np.sum(model.predict(X))/19 # change 19 to the corresponding  max_len(19 or 39)
    print(result)
