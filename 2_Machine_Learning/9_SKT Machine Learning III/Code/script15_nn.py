# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
%matplotlib inline

###########################################################
# Neural Network for Classification
###########################################################

# read data from file
df = pd.read_csv('data06_iris2.csv')
X = df.iloc[:,:-1]
Y = df['Species']
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=1) 

# neural network
from sklearn.neural_network import MLPClassifier
nn = MLPClassifier(
        hidden_layer_sizes = (2,2),
        activation = 'logistic',
        solver = 'lbfgs', # for small data set, sgd/adam for large data set
        alpha = 0.0001, # L2 regularization
        batch_size = 'auto',
        learning_rate = 'constant',
        learning_rate_init = 0.001,
        random_state = 0,
        max_iter = 1000)
nn.fit(xtrain,ytrain)
yhat_test = nn.predict(xtest)
yhat_test_prob = nn.predict_proba(xtest)
print(yhat_test)
nn.score(xtrain,ytrain)
nn.score(xtest,ytest)

nn.coefs_
nn.intercepts_

###########################################################
# Nueral Network for Regression
###########################################################

# read data
df = pd.read_csv('data07_diabetes.csv')
X = df.iloc[:,:-1]
y = df['Y']
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.33,random_state=1)

# neural network
from sklearn.neural_network import MLPRegressor
nn = MLPRegressor(
        hidden_layer_sizes = (2,2),
        activation = 'relu',
        solver = 'lbfgs', 
        alpha = 0.0001,
        batch_size = 'auto',
        learning_rate = 'constant',
        learning_rate_init = 0.001,
        random_state = 0,
        max_iter = 10000)
nn.fit(xtrain,ytrain)
yhat_test = nn.predict(xtest)
nn.score(xtrain,ytrain)
nn.score(xtest,ytest)

# tune the NN structure



###########################################################
# Practice
###########################################################


# practice
df = pd.read_csv('data08_khan.csv',header=None)
dfx = df.iloc[:,1:]
dfy = df.iloc[:,0]
xtrain, ytrain = dfx.iloc[:63,:], dfy[:63]
xtest, ytest = dfx.iloc[63:,:], dfy[63:]





























# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# read data
df = pd.read_csv('data08_khan.csv',header=None)
dfx = df.iloc[:,1:]
dfy = df.iloc[:,0]
xtrain, ytrain = dfx.iloc[:63,:], dfy[:63]
xtest, ytest = dfx.iloc[63:,:], dfy[63:]

# scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() 
scaler.fit(xtrain)
xtrain = scaler.transform(xtrain)
xtest = scaler.transform(xtest) 

# neural network classifier
from sklearn.neural_network import MLPClassifier
nn = MLPClassifier(
        hidden_layer_sizes = (100,50,30,10),
        activation = 'relu',
        solver = 'lbfgs', # for small data set, sgd/adam for large data set
        alpha = 1, # L2 regularization
        batch_size = 'auto',
        learning_rate = 'constant',
        learning_rate_init = 0.001,
        random_state = 0,
        max_iter = 1000)
nn.fit(xtrain,ytrain)
yhat_test = nn.predict(xtest)
nn.score(xtrain,ytrain)
nn.score(xtest,ytest)
pd.crosstab(yhat_test,ytest)

# neural network classifier
from sklearn.neural_network import MLPRegressor
nn = MLPRegressor(
        hidden_layer_sizes = (30,20,10),
        activation = 'relu',
        solver = 'lbfgs', # for small data set, sgd/adam for large data set
        alpha = 1, # L2 regularization
        batch_size = 'auto',
        learning_rate = 'constant',
        learning_rate_init = 0.001,
        random_state = 0,
        max_iter = 1000)
nn.fit(xtrain,ytrain)
yhat_test = nn.predict(xtest)
nn.score(xtrain,ytrain)
nn.score(xtest,ytest)
plt.plot(yhat_test,ytest,'go')

