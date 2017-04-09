"""
    function:
    k-fold cross validation
    """
__author__ = "Shiyi Li"

# sentence length(# of char)
# sentence length(# of words)
# # of punctuations
# # of illegal punctuations
import string
import numpy as np

def removePunc(input):
    '''
    :param input: string
    :return: string, without the punctuations
    '''
    return input.translate(string.maketrans("",""), string.punctuation)

def numOfWords(input):
    '''
    :param input: string
    :return: number of words, number of continuous space
    '''
    splitted = input.split(" ")
    res=0
    for i in splitted:
        if len(i)>0:
            res+=1
    return res

def numOfChar(input):
    '''
    :param input: string
    :return: number of char
    '''
    return len(input)

def numOfPunc(input):
    '''
    :param input: string
    :return: number of punctuations
    '''
    return len(input)-len(removePunc(input))

def numOfContPunc(input):
    res=0;
    state=False
    for i in range(1,len(input)):
        if input[i] in string.punctuation:
            if input[i-1] in string.punctuation:
                if state:
                    pass
                else:
                    state=True
                    res+=1
            else:
                state=False
                pass
        else:
            state=False
    return res

def constructMat(file,label):
    '''
    :param file: input file
    :param label: the label of the data in the file
    :return: ndarray
    '''
    res=np.array([])
    line1=True
    with open(file) as data:
        for line in data:
            if line1:
                line1=False
                cleaned = line.lower().strip()
                fea1 = numOfWords(cleaned)
                fea2 = numOfChar(cleaned)
                fea3 = numOfPunc(cleaned)
                fea4 = numOfContPunc(cleaned)
                res = np.array([[fea1, fea2, fea3, fea4, label]])
            else:
                cleaned = line.lower().strip()
                fea1 = numOfWords(cleaned)
                fea2 = numOfChar(cleaned)
                fea3 = numOfPunc(cleaned)
                fea4 = numOfContPunc(cleaned)
                newrow = np.array([[fea1, fea2, fea3, fea4, label]])
                res = np.append(res, newrow, axis=0)
    return res#.resize(5)#CHANGE THIS LINE!!!!!!!


if __name__ == '__main__':
    print constructMat('./fake_news_training.txt',1)