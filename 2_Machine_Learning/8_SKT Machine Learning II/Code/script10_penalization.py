# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# read data
df = pd.read_csv('data07_diabetes.csv')
X = df.iloc[:,:-1]
y = df['Y']

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.75,random_state=0)

# linear regression
from sklearn.linear_model import LinearRegression
f = LinearRegression()
f.fit(xtrain,ytrain)
f.intercept_,f.coef_
f.score(xtrain,ytrain)
f.score(xtest,ytest)

# ridge regression
from sklearn.linear_model import Ridge
f = Ridge(alpha=0.5)
f.fit(xtrain,ytrain)
f.intercept_,f.coef_
f.score(xtrain,ytrain)
f.score(xtest,ytest)

# lasso regression
from sklearn.linear_model import Lasso
f = Lasso(alpha=0.5)
f.fit(xtrain,ytrain)
f.intercept_,f.coef_
f.score(xtrain,ytrain)
f.score(xtest,ytest)

# Elastic Net regression
from sklearn.linear_model import ElasticNet
f = ElasticNet(alpha=0.1,l1_ratio=0.5)
f.fit(xtrain,ytrain)
f.intercept_,f.coef_
f.score(xtrain,ytrain)
f.score(xtest,ytest)

# select parameter using cross-validation
np.random.seed(0)
from sklearn.model_selection import cross_val_score
exp = np.linspace(-3,0,21)
alphas = 10**exp
s = np.zeros((len(alphas),3))
for n in range(s.shape[0]):
    f = Ridge(alpha=alphas[n])
    f.fit(xtrain,ytrain)
    s[n,0] = f.score(xtrain,ytrain)
    s[n,1] = cross_val_score(f,xtrain,ytrain,cv=5).mean()
    s[n,2] = f.score(xtest,ytest)

plt.plot(exp,s[:,0],exp,s[:,1],exp,s[:,2],marker='o')
plt.legend(('Train','CV','Test'))
plt.show()

idx = np.argmax(s[:,1])
f = Ridge(alpha=alphas[idx])
f.fit(xtrain,ytrain)
f.coef_
f.score(xtest,ytest)

# parameter tunning in short
np.random.seed(0)
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
f = RidgeCV(alphas=alphas,cv=5)
f.fit(xtrain,ytrain)
f.alpha_
f.coef_
f.score(xtest,ytest)


###########################################################
# Practice
###########################################################

# Practice 1

# Practice 2
df = pd.read_csv('data02_college.csv')
X = df.iloc[:,3:]
y = df['Accept']/df['Apps']
np.random.seed(1)
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.5,random_state=0)












































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# Practice 1

# LassoCV
np.random.seed(0)
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV
exp = np.linspace(-3,0,21)
alphas = 10**exp
f = LassoCV(alphas=alphas,cv=5)
f.fit(xtrain,ytrain)
f.score(xtest,ytest)

# ElasticNet CV
exp = np.linspace(-4,1,31)
alphas = 10**exp
ratios = np.linspace(0,1,11)
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import ElasticNetCV
f = ElasticNetCV(l1_ratio=ratios,alphas=alphas,cv=5)
f.fit(xtrain,ytrain)
f.score(xtest,ytest)



# Practice 2

df = pd.read_csv('data02_college.csv')
X = df.iloc[:,3:]
y = df['Accept']/df['Apps']
np.random.seed(1)
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.5,random_state=0)

# elastic net parameter search
exp = np.linspace(-4,1,31)
alphas = 10**exp
ratios = np.linspace(0,1,11)
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import ElasticNetCV
f = ElasticNetCV(l1_ratio=ratios,alphas=alphas,cv=5)
f.fit(xtrain,ytrain)
f.score(xtest,ytest)

# for comparison
from sklearn.linear_model import LinearRegression
f = LinearRegression()
f.fit(xtrain,ytrain)
f.score(xtest,ytest)








