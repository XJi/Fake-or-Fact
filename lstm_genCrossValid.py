import numpy as np
import math
import re
import nltk
from scipy import stats
from random import shuffle
from keras.preprocessing.text import one_hot
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout, Activation, Embedding


def transform_keywords(file_name):
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

def transform_titles(file_name):
    inf_file = open(file_name)
    data = list()
    for one_news in inf_file.readlines():
        single = nltk.word_tokenize(clean_sentence(one_news))
        print(single)
        mapping = list()
        for one_keyword in single:
            mapping.append(one_hot(one_keyword, 7000)[0])
        data.append(mapping)
    # print(data)
    return data

def clean_sentence(s):
    c = s.lower().strip()
    return re.sub('[^a-z ]', '', c)

'''
:param
    type: 0 indicates using the keywords from the content
          1 indicates using the titles
'''
def make_prediction(fake_file, real_file, type, unit_size = 10):
    if type == 0:
        fake_data = transform_keywords(fake_file)
        real_data = transform_keywords(real_file)
    else:
        fake_data = transform_titles(fake_file)
        real_data = transform_titles(real_file)
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
    print(max_len)
    for d in data:
        cur_len = len(d)
        while cur_len < max_len:
            d.append(0)
            cur_len = cur_len+1
    print(data)

    #shuffle the given data
    index_shuf = list(range(len(data)))
    shuffle(index_shuf)
    data_shuffled = list()
    label_shuffled = list()
    for i in index_shuf:
        data_shuffled.append(data[i])
        label_shuffled.append(labels[i])
    print(len(label_shuffled))
    print(label_shuffled)

    # generate cross validation datasets
    k = 0
    testing_size = len(data_shuffled)/unit_size
    training_set_X = list()
    training_set_Y = list()
    testing_set_X = list()
    testing_set_Y = list()

    while k < testing_size:
        test_X= data_shuffled[k*unit_size:(k+1)*unit_size]
        test_Y = label_shuffled[k*unit_size:(k+1)*unit_size]

        train_X = data_shuffled[:k * unit_size] + data_shuffled[(k + 1) * unit_size:]
        train_Y = label_shuffled[:k * unit_size] + label_shuffled[(k + 1) * unit_size:]

        training_set_X.append(train_X)
        training_set_Y.append(train_Y)
        testing_set_X.append(test_X)
        testing_set_Y.append(test_Y)
        k = k+1

    print(len(training_set_X))
    print(training_set_Y)

    # testing with the baseline
    test_index = 0
    while test_index < testing_size:
        print('Build model...')
        baselineTest = np.float(np.sum(testing_set_Y[test_index])) / unit_size
        model = Sequential()
        model.add(Embedding(7000, 256, dropout=0.2))
        model.add(LSTM(16, dropout_W=0.2, dropout_U=0.2))  # try using a GRU instead, for fun
        model.add(Dense(1))
        model.add(Activation('sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        print('Train...')
        model.fit(training_set_X[test_index], training_set_Y[test_index], batch_size=len(testing_set_X[test_index]),
                  nb_epoch=10,
                  validation_data=(testing_set_X[test_index], testing_set_Y[test_index]), shuffle=False)
        score, acc = model.evaluate(testing_set_X[test_index], testing_set_Y[test_index],
                                    batch_size=len(testing_set_X[test_index]))
        print('Test accuracy:', acc)
        print('Baseline: ', str(max(baselineTest,1-baselineTest)))
        test_index = test_index +1

if __name__ == "__main__":
    #Task on the content keywords
    make_prediction("./fakenews_keywords.csv","./realnews_keywords.csv",0)
    #Task on the titles
    #make_prediction("./data/titles/fake_news_training.txt", "./data/titles/real_news_training.txt",1 )