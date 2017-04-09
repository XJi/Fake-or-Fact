"""
    function:
    1. k-fold cross validation
    2. automatically fit the better parameter based on cross-validation
    """
__author__ = "Shiyi Li"

import numpy as np
import math
import RandomTree as rt
import RandomForest as rf#bag learner
import genCrossValid as gc #generate cross-validation

def getCrossValidSet(k=10, file="./data.csv", writeToFile=False):
    train,test=gc.genData(k=10, file="./data.csv", writeToFile=True)
    return train,test

def run(train=[],test=[],leafsize=5,bag=10):
    print
    print
    for cv in range(0,10):
        traindata = train[cv];
        testdata = test[cv];
        trainX = traindata[:, 0:-1]
        trainY = traindata[:, -1]
        testX = testdata[:, 0:-1]
        testY = testdata[:, -1]
        learner = rf.RandomForest(learner=rt.RandomTree, kwargs={"leaf_size": leafsize}, bags=bag, boost=False,
                                verbose=False)
        learner.addEvidence(trainX, trainY)
        inSamY = learner.query(trainX)#in sample test
        outSamY = learner.query(testX)#out sample test
        sizeTrainSet=len(trainX)#how many data in this train set
        sizeTestSet=len(testX)#how many data in this test set
        baselineTrain=np.sum(trainY)/sizeTrainSet
        baselineTest=np.sum(testY)/sizeTestSet
        #print np.sum(inSamY==trainY)
        inSamACC=np.sum(inSamY==trainY)
        outSamACC=np.sum(outSamY==testY)
        print "================"
        print "doing cross-valid "+str(cv+1)+":"
        print "in-sample error: "+str(inSamACC)
        print "in-sample baseline 1: "+str(baselineTrain)
        print "in-sample baseline 2: "+str(1-baselineTrain)
        print "out-sample error: "+str(outSamACC)
        print "out-sample baseline 1: "+str(baselineTest)
        print "out-sample baseline 2: "+str(1-baselineTest)
        print

if __name__=="__main__":
    #run(17,15);#(leaf,bag)
    train,test=getCrossValidSet(k=10, file="./data.csv", writeToFile=True)
    run(train,test,5,1)
    pass;