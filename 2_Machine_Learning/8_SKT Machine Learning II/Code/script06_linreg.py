# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# read data
df = pd.read_csv('data05_boston.csv')

# simple linear regression
from sklearn.linear_model import LinearRegression
X = df[['lstat']]
y = df['medv']
lm = LinearRegression()
lm.fit(X,y)
lm.coef_  # coefficients
lm.intercept_ # intercepter
yhat = lm.predict(X) # prediction

r2 = lm.score(X,y) # R2
rmse = np.sqrt( ((yhat-y)**2).mean() ) # RMSE

plt.plot(X,y,'bo')
plt.plot(X,yhat,'r',linewidth=2)
plt.title('%s vs. Medv: %.2f' % ('lstat',r2))
plt.show()

# multiple linear regression
X = df.iloc[:,:-1]
y = df['medv']
lm = LinearRegression()
lm.fit(X,y)
lm.coef_  # coefficients
lm.intercept_ # intercepter
yhat = lm.predict(X) # prediction
lm.score(X,y) # R2
np.sqrt( ((yhat-y)**2).mean() ) # RMSE

plt.plot(yhat,y,'bo')
plt.title('All vs. Medv: %.2f' % r2)
plt.show()

# add a new variable: 2nd-order term
X = df[['lstat']]
X['lstat2'] = X['lstat']**2
y = df['medv']
lm = LinearRegression()
lm.fit(X,y)
lm.score(X,y)
np.sqrt( ((yhat-y)**2).mean() ) # RMSE

# add a new variable: interaction term
X = df[ ['lstat','rm'] ]
X['lstat_rm'] = X['lstat'] * X['rm']
y = df['medv']
lm = LinearRegression()
lm.fit(X,y)
lm.score(X,y)
np.sqrt( ((yhat-y)**2).mean() ) # RMSE

# training & test
X = df.iloc[:,:-1]
Y = df['medv']
from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,Y,test_size=0.75,random_state=1) 

lm = LinearRegression()
lm.fit(Xtrain,Ytrain)
lm.score(Xtrain,Ytrain)
lm.score(Xtest,Ytest)

Xtrain_sub = Xtrain.iloc[:,[0,1,3,4,5,7,8,9,10,11,12]]
Xtest_sub = Xtest.iloc[:,[0,1,3,4,5,7,8,9,10,11,12]]
lm = LinearRegression()
lm.fit(Xtrain_sub,Ytrain)
lm.score(Xtrain_sub,Ytrain)
lm.score(Xtest_sub,Ytest)



###########################################################
# Practice 
###########################################################

# data01_iris.csv를 읽으시오. 
# Sepal Width ~ Sepal.Length + Petal.Length + Petal.Width 로 
# 선형 회귀 분석을 수행하시오. 
# (1) R2와 RMSE 값은 얼마인가?
# (2) 어떤 변수의 제곱항을 추가하였을 때, 가장 높은 R2를 갖는 것은 어느 변수인가?
# (3) Sepal.Length와 Petal.Length의 interaction 항을 추가하였을 때, R2은 
# 얼마인가?
# (4) 범주형 변수 Sepcies를 포함시켜 선형 회귀 분석을 수행하시오.



















# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# practice
df = pd.read_csv('data01_iris.csv')

# (1)
X = df[['Sepal.Length','Petal.Length','Petal.Width']]
y = df['Sepal.Width']

lm = LinearRegression()
lm.fit(X,y)
lm.score(X,y)
np.sqrt( ((lm.predict(X)-y)**2).mean() )

# (2)
X = df[['Sepal.Length','Petal.Length','Petal.Width']]
y = df['Sepal.Width']
x1 = X['Petal.Width']**2
X['PW2'] = x1

lm.fit(X,y)
lm.score(X,y)
np.sqrt( ((lm.predict(X)-y)**2).mean() )

# (3)
X = df[['Sepal.Length','Petal.Length','Petal.Width']]
y = df['Sepal.Width']
x1 = X['Petal.Width']*X['Petal.Length']
X['Inter'] = x1

lm.fit(X,y)
lm.score(X,y)
np.sqrt( ((lm.predict(X)-y)**2).mean() )

# (4)
X = df[['Sepal.Length','Petal.Length','Petal.Width']]

x1 = pd.Series(np.zeros(X.shape[0]))
x1[ df['Species']=='setosa' ] = 1
x2 = pd.Series(np.zeros(X.shape[0]))
x2[ df['Species']=='virginica' ] = 1

X['Species_setosa'] = x1
X['Species_virginica'] = x2
y = df['Sepal.Width']

lm.fit(X,y)
lm.score(X,y)
np.sqrt( ((lm.predict(X)-y)**2).mean() )

