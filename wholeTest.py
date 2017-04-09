"""
    function:
    k-fold cross validation
    """
__author__ = "Shiyi Li"

import numpy as np
import math
import RandomTree as rt
import RandomForest as rf#bag learner
import genCrossValid as gc #generate cross-validation
from sklearn import tree
from sklearn.svm import SVC

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
        sizeTrainSet=len(trainX)#how many data in this train set
        sizeTestSet=len(testX)#how many data in this test set
        baselineTrain=np.float(np.sum(trainY))/sizeTrainSet
        baselineTest=np.float(np.sum(testY))/sizeTestSet
        #print np.sum(inSamY==trainY)

        # ========================
        #Random Forest
        learner = rf.RandomForest(learner=rt.RandomTree, kwargs={"leaf_size": leafsize}, bags=bag, boost=False,
                                verbose=False)
        learner.addEvidence(trainX, trainY)
        inSamY = learner.query(trainX)#in sample test
        outSamY = learner.query(testX)#out sample test
        inSamACC=np.float(np.sum(inSamY==trainY))/sizeTrainSet
        outSamACC=np.float(np.sum(outSamY==testY))/sizeTestSet

        # ========================
        #Decision Tree
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(trainX, trainY)
        DTinSamY = clf.predict(trainX)
        DToutSamY = clf.predict(testX)
        DTinSamACC = np.float(np.sum(DTinSamY == trainY)) / sizeTrainSet
        DToutSamACC = np.float(np.sum(DToutSamY == testY)) / sizeTestSet

        # ========================
        #SVM
        svm = SVC()
        svm.fit(trainX, trainY)
        SVMinSamY = svm.predict(trainX)
        SVMoutSamY = svm.predict(testX)
        SVMinSamACC = np.float(np.sum(SVMinSamY == trainY)) / sizeTrainSet
        SVMoutSamACC = np.float(np.sum(SVMoutSamY == testY)) / sizeTestSet


        print "================"
        print "doing cross-valid "+str(cv+1)+":"
        print "in-sample Accuracy baseline: "+str(max(baselineTrain,1-baselineTrain))
        print "in-sample Accuracy - Random Forest: " + str(inSamACC)
        print "in-sample Accuracy - Decision Tree: " + str(DTinSamACC)
        print "in-sample Accuracy - SVM: " + str(SVMinSamACC)
        print "out-sample Accuracy baseline: "+str(max(baselineTest,1-baselineTest))
        print "out-sample Accuracy - Random Fotrest: "+str(outSamACC)
        print "out-sample Accuracy - Decision Tree: " + str(DToutSamACC)
        print "out-sample Accuracy - SVM: " + str(SVMoutSamACC)
        print

if __name__=="__main__":
    #run(17,15);#(leaf,bag)
    train,test=getCrossValidSet(k=10, file="./data.csv", writeToFile=False)
    run(train,test,5,10)
    pass;