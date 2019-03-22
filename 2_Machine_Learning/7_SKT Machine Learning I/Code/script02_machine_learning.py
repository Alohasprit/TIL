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
# Practice 
###########################################################

# colleage 데이터 셋을 읽어 Private을 다른 변수를 이용하여 KNN 방식으로 예측하시오. 
# 이때, Train와 Test 셋을 나누고 Train 셋을 이용하여 모델을 학습하시오.
# train_test_split을 이용하여 나누되 test_size=0.4, random_state=0를 이용하시오.
# K=1, K=10, K=20 에 대하여 train/test accuracy를 구하고 
# 결과를 모델의 유연성과 관련지어 생각해보시오.

# K를 1부터 20까지 변화시키가며 train/test accuracy의 그래프를 그리시오































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################


import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv('data02_college.csv')
X = df.iloc[:,2:]
Y = df['Private']
xtrain, xtest, ytrain, ytest = train_test_split(X,Y,test_size=0.4,random_state=0) 


f = KNeighborsClassifier(1)
f.fit(xtrain,ytrain)
print(f.score(xtrain,ytrain),f.score(xtest,ytest))


Klist = np.arange(1,21)
acclist_train = np.zeros(20)
acclist_test = np.zeros(20)
for i in range(20):
    f = KNeighborsClassifier(Klist[i])
    f.fit(xtrain,ytrain)
    acc_test = f.score(xtest,ytest)
    acc_train = f.score(xtrain,ytrain)    
    acclist_train[i] = acc_train
    acclist_test[i] = acc_test

plt.plot(Klist,acclist_train,'b-')
plt.plot(Klist,acclist_test,'r-')



