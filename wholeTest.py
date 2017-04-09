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
import string
import feature
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

def getCrossValidSet(k=10, file="./data.csv", writeToFile=True):
    train,test=gc.genData(k, file, writeToFile)
    return train,test

def run(train=[],test=[],leafsize=5,bag=10):
    print
    print
    #overall accuracy
    RFACCout = 0.0
    DTACCout = 0.0
    SVMACCout = 0.0
    RFCACCout=0.0
    MLPACCout = 0.0
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
        #inSamY = learner.query(trainX)#in sample test
        outSamY = learner.query(testX)#out sample test
        #inSamACC=np.float(np.sum(inSamY==trainY))/sizeTrainSet
        outSamACC=np.float(np.sum(outSamY==testY))/sizeTestSet
        #RFACCin = RFACCin + inSamACC
        RFACCout = RFACCout + outSamACC

        # ========================
        #Random Forest - SKLEARN
        rfc=RandomForestClassifier(n_estimators=bag)
        rfc.fit(trainX, trainY)
        RFCoutSamY=rfc.predict(testX)
        RFCoutSamACC = np.float(np.sum(RFCoutSamY == testY)) / sizeTestSet
        RFCACCout=RFCACCout+RFCoutSamACC

        # ========================
        #Decision Tree
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(trainX, trainY)
        #DTinSamY = clf.predict(trainX)
        DToutSamY = clf.predict(testX)
        #DTinSamACC = np.float(np.sum(DTinSamY == trainY)) / sizeTrainSet
        DToutSamACC = np.float(np.sum(DToutSamY == testY)) / sizeTestSet
        #DTACCin = DTACCin + DTinSamACC
        DTACCout = DTACCout + DToutSamACC

        # ========================
        #SVM
        svm = SVC()
        svm.fit(trainX, trainY)
        #SVMinSamY = svm.predict(trainX)
        SVMoutSamY = svm.predict(testX)
        #SVMinSamACC = np.float(np.sum(SVMinSamY == trainY)) / sizeTrainSet
        SVMoutSamACC = np.float(np.sum(SVMoutSamY == testY)) / sizeTestSet
        #SVMACCin = SVMACCin + SVMinSamACC
        SVMACCout = SVMACCout + SVMoutSamACC

        # ========================
        # feed forward - neural net
        clf=MLPClassifier(solver='lbfgs',alpha=1e-5,hidden_layer_sizes=(100,), random_state=1)
        clf.fit(trainX, trainY)
        MLPoutSamY = clf.predict(testX)
        MLPoutSamACC = np.float(np.sum(MLPoutSamY == testY)) / sizeTestSet
        MLPACCout = MLPACCout+ MLPoutSamACC


        print "================"
        print "doing cross-valid "+str(cv+1)+":"
        #print "in-sample Accuracy baseline: "+str(max(baselineTrain,1-baselineTrain))
        #print "in-sample Accuracy - Random Forest: " + str(inSamACC)
        #print "in-sample Accuracy - Decision Tree: " + str(DTinSamACC)
        #print "in-sample Accuracy - SVM: " + str(SVMinSamACC)
        print "out-sample Accuracy baseline: "+str(max(baselineTest,1-baselineTest))
        print "out-sample Accuracy - Random Forest: "+str(outSamACC)
        print "out-sample Accuracy - Random Forest - SKLEARN: "+str(RFCoutSamACC)
        print "out-sample Accuracy - Decision Tree: " + str(DToutSamACC)
        print "out-sample Accuracy - SVM: " + str(SVMoutSamACC)
        print "out-sample Accuracy - Neural Net MLP: "+str(MLPoutSamACC)
        print

    print
    print "================================"
    print "cross validation done"
    print "Out-sample accuracy: "
    print "Random Forest: "+str(RFACCout/10)
    print "Random Forest - SKLEARN: "+str(RFCACCout/10)
    print "Decision Tree: "+str(DTACCout/10)
    print "SVM: "+str(SVMACCout/10)
    print "Neural Net MLP: "+str(MLPACCout/10)

if __name__=="__main__":
    #run(17,15);#(leaf,bag)
    #train,test=getCrossValidSet(k=10, file="./data.csv", writeToFile=False)
    #run(train,test,5,10)
    real=feature.constructMat('./real2.txt', 1)
    fake=feature.constructMat('./fake2.txt', 0)
    data=np.append(real,fake,axis=0)
    np.random.shuffle(data)
    np.savetxt("data.csv", data, delimiter=",")
    train, test = getCrossValidSet(k=10, file="./data.csv", writeToFile=False)
    run(train, test, 5, 30)