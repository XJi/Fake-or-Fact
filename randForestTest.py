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

def getCrossValidSet(k=10, file="./data.csv", writeToFile=True):
    train,test=gc.genData(k, file, writeToFile)
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
        baselineTrain=np.float(np.sum(trainY))/sizeTrainSet
        baselineTest=np.float(np.sum(testY))/sizeTestSet
        #print np.sum(inSamY==trainY)
        inSamACC=np.float(np.sum(inSamY==trainY))/sizeTrainSet
        outSamACC=np.float(np.sum(outSamY==testY))/sizeTestSet
        print "================"
        print "doing cross-valid "+str(cv+1)+":"
        print "in-sample Accuracy: "+str(inSamACC)
        print "in-sample baseline: "+str(max(baselineTrain,1-baselineTrain))
        print "out-sample Accuracy: "+str(outSamACC)
        print "out-sample baseline: "+str(max(baselineTest,1-baselineTest))
        print

if __name__=="__main__":
    #run(17,15);#(leaf,bag)
    train,test=getCrossValidSet(k=10, file="./data.csv", writeToFile=False)
    run(train,test,5,10)
    pass;