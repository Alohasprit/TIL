# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
%matplotlib inline

###########################################################
# Classification Tree
###########################################################

# read data from file
df = pd.read_csv('data01_iris.csv')
X = df.iloc[:,:-1]
Y = df['Species']
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=1) 

# classification tree
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()
clf.fit(xtrain,ytrain)
yhat_train = clf.predict(xtrain)
yhat_train_prob = clf.predict_proba(xtrain)
yhat_test = clf.predict(xtest)
yhat_test_prob = clf.predict_proba(xtest)
clf.score(xtrain,ytrain)
clf.score(xtest,ytest)

# lda for comparison
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis()
lda.fit(xtrain,ytrain)
lda.score(xtrain,ytrain)
lda.score(xtest,ytest)

# make data dirty
np.random.seed(0)
xtrain2 = xtrain + np.random.randn(np.prod(xtrain.shape)).reshape(90,4)
xtest2 = xtest + np.random.randn(np.prod(xtest.shape)).reshape(60,4)

# classification tree
clf = DecisionTreeClassifier(max_leaf_nodes=None) # change max_leaef_nodes
clf.fit(xtrain2,ytrain)
clf.score(xtrain2,ytrain)
clf.score(xtest2,ytest)

# visualization
from sklearn.tree import export_graphviz
export_graphviz(clf,out_file='tree.dot', max_depth=None,
                feature_names=xtrain.columns,
                class_names=['setosa','versicolor','virginica'])
# to visualize, use http://www.webgraphviz.com/ or other tools


###########################################################
# Regression Tree
###########################################################

# read data
df = pd.read_csv('data05_boston.csv')
X, Y = df.iloc[:,:-1], df['medv']
xtrain,xtest,ytrain,ytest = train_test_split(X,Y,test_size=0.33,random_state=0)

# regression tree
from sklearn.tree import DecisionTreeRegressor
clf = DecisionTreeRegressor(max_leaf_nodes=None) # change max_leaf_nodes
clf.fit(xtrain,ytrain)
clf.score(xtrain,ytrain)
clf.score(xtest,ytest)

# linear regression
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(xtrain,ytrain)
lm.score(xtrain,ytrain)
lm.score(xtest,ytest)

# visualization
from sklearn.tree import export_graphviz
export_graphviz(clf,out_file='tree.dot', max_depth=None,
                feature_names=xtrain.columns,
                class_names=['setosa','versicolor','virginica'])
# to visualize, use http://www.webgraphviz.com/ or other tools



###########################################################
# Practice
###########################################################







































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# read data
df = pd.read_csv('data05_boston.csv')
X, Y = df.iloc[:,:-1], df['medv']
xtrain,xtest,ytrain,ytest = train_test_split(X,Y,test_size=0.33,random_state=0)

# cross-validation
np.random.seed(0)
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
s = np.zeros((100,3))
for n in range(s.shape[0]):
    f = DecisionTreeRegressor(max_leaf_nodes=n+2,random_state=None)
    f.fit(xtrain,ytrain)
    s[n,0] = f.score(xtrain,ytrain)
    s[n,1] = cross_val_score(f,xtrain,ytrain,cv=5).mean()
    s[n,2] = f.score(xtest,ytest)

plt.plot(s,marker='o')
plt.legend(('Train','CV','Test'))
plt.show()



