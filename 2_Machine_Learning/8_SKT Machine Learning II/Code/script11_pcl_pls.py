# libraries
import numpy as np
import scipy as sp
import pandas as pd

# read data
df = pd.read_csv('data05_boston.csv')
X = df.iloc[:,:-1]
y = df['medv']

# ordinary linear regression
from sklearn.linear_model import LinearRegression
f = LinearRegression()
f.fit(X,y) # all 13 X's
f.score(X,y)
X2 = X[['crim','zn','indus']]
#X2 = X[['lstat','age','rm']]
f.fit(X2,y)
f.score(X2,y)

# pcr
from sklearn.decomposition import PCA
pca = PCA(n_components=3)
Xtrans = pca.fit_transform(X)
f = LinearRegression()
f.fit(Xtrans,y)
f.score(Xtrans,y)

pca = PCA(n_components=13)
Xtrans = pca.fit_transform(X)
f = LinearRegression()
f.fit(Xtrans,y)
f.score(Xtrans,y)

from sklearn.preprocessing import scale
Xscaled = scale(X,axis=0,with_mean=True,with_std=True)
pca = PCA(n_components=3)
Xtrans = pca.fit_transform(Xscaled)
f = LinearRegression()
f.fit(Xtrans,y)
f.score(Xtrans,y)

# pls
from sklearn.cross_decomposition import PLSRegression
f = PLSRegression(n_components=3) # first 3 PCs
f.fit(X,y)
f.score(X,y)
f = PLSRegression(n_components=13) # all 13 components
f.fit(X,y)
f.score(X,y)


###########################################################
# Practice
###########################################################











































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

df = pd.read_csv('data05_diabetes.csv')
X = df.iloc[:,:-1]
y = df['Y']

# linear regression
f = LinearRegression()
f.fit(X,y)
f.score(X,y)

# pcr
pca = PCA(n_components=2)
Xtrans = pca.fit_transform(X)
f = LinearRegression()
f.fit(Xtrans,y)
f.score(Xtrans,y)

# pls
f = PLSRegression(n_components=2)
f.fit(X,y)
f.score(X,y)










