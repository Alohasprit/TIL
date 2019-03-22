# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# read data from file
df = pd.read_csv('data01_iris.csv')
X = df.iloc[:,:-1]
Y = df['Species']

# separating train & test sets
from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 

# K-fold CV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score
f = LinearDiscriminantAnalysis()
f.fit(xtrain,ytrain)
f.score(xtrain,ytrain)
f.score(xtest,ytest)
s = cross_val_score(f,xtrain,ytrain,cv=3)
s.mean()


###########################################################
# Practice
###########################################################

df = pd.read_csv('data06_iris2.csv')
X = df.iloc[:,:-1]
Y = df['Species']
from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 

# plot train, test, and 5-fold cross-validation errors of KNN according to N





























# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

df = pd.read_csv('data05_iris.csv')
X = df.iloc[:,:-1]
Y = df['Species']
from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 

from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

s = np.zeros((40,3))
for n in range(s.shape[0]):
    f = KNeighborsClassifier(n+1)
    f.fit(xtrain,ytrain)
    s[n,0] = f.score(xtrain,ytrain)
    s[n,1] = cross_val_score(f,xtrain,ytrain,cv=5).mean()
    s[n,2] = f.score(xtest,ytest)
    
plt.plot(np.arange(1,41),1-s,marker='o')
plt.legend(('Train','CV','Test'))
plt.show()





