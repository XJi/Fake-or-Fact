import re
# import nltk
import numpy as np
# from keras.preprocessing.text import one_hot
from sklearn import tree
from sklearn import svm
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

# test Decision Tree and compare with SVM
# use two feature: title length and special character

def clean_sentence(s):
    c = s.lower().strip()
    return c

def count_special_character(sentences):
    l = list(sentences)
    count = 0
    flag = 0
    for ch in l:
        if (ch == '!') or (ch == '?') or (ch == '|'):
            count = count + 1
        if ch == '.':
            if flag == 0:
                flag = 1
            else:
                count = count + 1
                flag = 0
    return count

def count_length(sentences):
    return len(sentences)

def set_label(fake_size, real_size):
    label = list()
    for counter in range(0,fake_size):
        label.append(0)
    for counter in range(0,real_size):
        label.append(1)
    return label

train_news = list()
fake_size = 0
real_size = 0
with open('./data/fake_news_training.txt') as train1:
    with open('./data/real_news_training.txt') as train2:
        for line in train1:
            special_character = count_special_character(clean_sentence(line))
            line_length = count_length(clean_sentence(line))
            train_news.append([special_character, line_length])
            fake_size = fake_size+1
        for line in train2:
            special_character = count_special_character(clean_sentence(line))
            line_length = count_length(clean_sentence(line))
            train_news.append([special_character, line_length])
            real_size = real_size+1

predict_news = list()
with open('./data/testing_real.txt') as predict1:
    with open('./data/testing_fake.txt') as predict2:
        for line in predict1:
            special_character = count_special_character(clean_sentence(line))
            line_length = count_length(clean_sentence(line))
            predict_news.append([special_character, line_length])
        for line in predict2:
            special_character = count_special_character(clean_sentence(line))
            line_length = count_length(clean_sentence(line))
            predict_news.append([special_character, line_length])

labels = set_label(fake_size, real_size)


print labels
print train_news
print "test result with [R, R, R, R, F, F, F, F]"
print "Decision Tree Result: (1 for Real, 0 for fake)"
clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_news, labels)
print clf.predict(predict_news)

print "SVM Result: (1 for Real, 0 for fake)"
classif = OneVsRestClassifier(estimator=SVC(random_state=0))
print classif.fit(train_news, labels).predict(predict_news)
