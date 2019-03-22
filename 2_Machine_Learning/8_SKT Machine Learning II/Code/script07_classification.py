# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# read data from file
df = pd.read_csv('data06_iris2.csv')
X = df.iloc[:,:-1]
Y = df['Species']

# train & test data
from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=1) 


###########################################################
# logistic regression
###########################################################

from sklearn.linear_model import LogisticRegression

# multiple logistic regression
f = LogisticRegression()
f.fit(xtrain,ytrain)
yhat_train = f.predict(xtrain)
yhat_train_prob = f.predict_proba(xtrain)
yhat_test = f.predict(xtest)
yhat_test_prob = f.predict_proba(xtest)

pd.crosstab(ytrain,yhat_train)
pd.crosstab(ytest,yhat_test)

f.score(xtrain,ytrain)
f.score(xtest,ytest)

# roc curve
from sklearn.metrics import roc_curve, roc_auc_score
fpr,tpr,th = roc_curve(ytest,yhat_test_prob[:,1])

auc = roc_auc_score(ytest,yhat_test_prob[:,1])

plt.plot(fpr,tpr)
plt.title('AUC: %.2f' % auc)
plt.show()


###########################################################
# linear discriminant analysis
###########################################################

# linear discriminant analysis: 2D
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# full model
f = LinearDiscriminantAnalysis()
f.fit(xtrain,ytrain)
yhat_train = f.predict(xtrain)
yhat_train_prob = f.predict_proba(xtrain)
yhat_test = f.predict(xtest)
yhat_test_prob = f.predict_proba(xtest)
f.score(xtrain,ytrain)
f.score(xtest,ytest)

# roc
fpr,tpr,th = roc_curve(ytest,yhat_test_prob[:,1])
auc = roc_auc_score(ytest,yhat_test_prob[:,1])
plt.plot(fpr,tpr)
plt.title('AUC: %.2f' % auc)
plt.show()

# quadratic discriminant analysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

f = QuadraticDiscriminantAnalysis()
f.fit(xtrain,ytrain)
yhat_test = f.predict(xtest)
yhat_test_prob = f.predict_proba(xtest)
f.score(xtrain,ytrain)
f.score(xtest,ytest)

# roc
fpr,tpr,th = roc_curve(ytest,yhat_test_prob[:,1])
auc = roc_auc_score(ytest,yhat_test_prob[:,1])
plt.plot(fpr,tpr)
plt.title('AUC: %.2f' % auc)
plt.show()

###########################################################
# knn
###########################################################

from sklearn.neighbors import KNeighborsClassifier

f = KNeighborsClassifier(5)
f.fit(xtrain,ytrain)
yhat_test = f.predict(xtest)
yhat_test_prob = f.predict_proba(xtest)
f.score(xtrain,ytrain)
f.score(xtest,ytest)

# roc
fpr,tpr,th = roc_curve(ytest,yhat_test_prob[:,1])
auc = roc_auc_score(ytest,yhat_test_prob[:,1])
plt.plot(fpr,tpr)
plt.title('AUC: %.2f' % auc)
plt.show()

# Test set에서의 성능이 가장 좋은 K는?

###########################################################
# Multi-class classification
###########################################################

df = pd.read_csv('data05_diabetes.csv')
X = df.iloc[:,:-1]
Y = pd.cut(df['Y'],3,labels=[0,1,2])
Y.value_counts()
Y = Y.astype(dtype='int')
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=1) 

f = LinearDiscriminantAnalysis()
f.fit(xtrain,ytrain)
yhat_train = f.predict(xtrain)
yhat_train_prob = f.predict_proba(xtrain)
yhat_test = f.predict(xtest)
yhat_test_prob = f.predict_proba(xtest)

pd.crosstab(ytrain,yhat_train)
pd.crosstab(ytest,yhat_test)

f.score(xtrain,ytrain)
f.score(xtest,ytest)


###########################################################
# All at once
###########################################################

classifiers = [
    LogisticRegression(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis(),
    KNeighborsClassifier(5)]

for i in range(len(classifiers)):
    f = classifiers[i]
    f.fit(xtrain,ytrain)
    print(f.score(xtrain,ytrain),f.score(xtest,ytest))


###########################################################
# Practices
###########################################################

df = pd.read_csv('data02_college.csv')
X = df.iloc[:,2:]
Y = df['Private'].factorize()[0]
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 







































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################
df = pd.read_csv('data02_college.csv')
X = df.iloc[:,2:]
Y = df['Private'].factorize()[0]
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 

f = LogisticRegression()
f.fit(xtrain,ytrain)
f.score(xtrain,ytrain)
f.score(xtest,ytest)
yhat_test_prob = f.predict_proba(xtest)

fpr,tpr,th = roc_curve(ytest,yhat_test_prob[:,1])
auc = roc_auc_score(ytest,yhat_test_prob[:,1])
plt.plot(fpr,tpr)
