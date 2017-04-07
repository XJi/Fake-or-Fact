# Fake-or-Fact
A News Analyzer to detect fake news

### If you want to generate the data set for cross-validation  
[wikipedia for cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics))  
in genCrossValid.py, <b>genData(k, file, writeToFile)</b> can generate the datasets for k-fold cross validation  
<b>--parameters</b>  
<b>k</b>: number of folds, fedault 10  
<b>file</b>: the path of the file  
<b>writeToFile</b>: Boolean, wether write the cross-validation data to files or not. If true, the method will generate 2*k files, where "ntrain.csv" contains the training set for n-th cross validation and "ntest.csv" contains the testing set for n-th cross-validation  
<b>--return</b>: list for training sets and list of testing sets (all in Numpy's nd-array)


### prerequisite outside libraries  
if using RandomTree.py, RandomForest.py, genCrossValid.py, then <b>Numpy</b> and <b>Scipy</b> are required:  
Numpy v1.11.1  
Scipy v0.17.1  
  
  
