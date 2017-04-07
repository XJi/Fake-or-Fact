# Fake-or-Fact
A News Analyzer to detect fake news

### If you want to generate the data set for cross-validation  
in genCrossValid.py, genData(k, file, writeToFile) can generate the datasets for k-fold cross validation  
k: number of folds, fedault 10  
file: the path of the file  
writeToFile: boolean, wether write the cross-validation data to files. If true, the method will generate 2*k files, where "ntrain.csv" contains the training set for n-th cross validation and "ntest.csv" contains the testing set for n-th cross-validation  
  
return: list for training sets and list of testing sets (all in Numpy's nd-array)


### prerequisite libraries  
if using RandomTree.py, RandomForest.py, genCrossValid.py, then Numpy % scipy are required:  
Numpy v1.11.1  
Scipy v0.17.1  
