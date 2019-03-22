# libraries
import numpy as np
import scipy as sp
import pandas as pd

# read data from file
df = pd.read_csv('data01_iris.csv')
X = df.iloc[:,:-1]
Y = df['Species']

# train & test data
from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 

###########################################################
# K-nearest neighbor
###########################################################

from sklearn.neighbors import KNeighborsClassifier

f = KNeighborsClassifier(20)
f.fit(xtrain,ytrain)
ytrain_hat = f.predict(xtrain)
ytest_hat = f.predict(xtest)

pd.crosstab(ytrain,ytrain_hat)
pd.crosstab(ytest,ytest_hat)

f.score(xtrain,ytrain)
f.score(xtest,ytest)

# 퀴즈: train score와 test score가 각각 가장 높은 K값은?



###########################################################
# Naive Bayesian
###########################################################

# GaussianNB
from sklearn.naive_bayes import GaussianNB

f = GaussianNB()
f.fit(xtrain,ytrain)
ytrain_hat = f.predict(xtrain)
ytest_hat = f.predict(xtest)

pd.crosstab(ytrain,ytrain_hat)
pd.crosstab(ytest,ytest_hat)

f.score(xtrain,ytrain)
f.score(xtest,ytest)



###########################################################
# Practice 
###########################################################

df = pd.read_csv('data02_college.csv')
X = df.iloc[:,2:]
Y = df['Private']
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 


































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF


###########################################################
# Practice 
###########################################################

df = pd.read_csv('data02_college.csv')
X = df.iloc[:,2:]
Y = df['Private']
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 

f = KNeighborsClassifier(5)
f.fit(xtrain,ytrain)
f.score(xtest,ytest)
f.score(xtrain,ytrain)
ytest_hat = f.predict(xtest)
pd.crosstab(ytest,ytest_hat)

