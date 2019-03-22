# libraries
import numpy as np
import scipy as sp
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt

# read csv file
iris = pd.read_csv('data01_iris.csv')

###########################################################
# one-sample t-test
###########################################################

d = np.array([-0.31,-0.67,-0.61,-2.07,-1.31])
r = sp.stats.ttest_1samp(d,0)
r.pvalue

# data01_iris.csv 에서 setosa 품종의 평균 Sepal Length가 4가 아니라는 
# 가설에 대한 p-value를 구하시오.



###########################################################
# two-sample t-test
###########################################################

np.random.seed(1)
x1 = np.random.normal(0.5,1,10)
x2 = np.random.normal(-0.5,1,10)
r = sp.stats.ttest_ind(x1,x2)
r.pvalue
# what is the number of samples for pvalue < 0.01

iris1 = iris[ iris['Species']=='versicolor' ]
iris2 = iris[ iris['Species']=='setosa' ]
sp.stats.ttest_ind(iris1['Sepal.Length'],iris2['Sepal.Length'])

# what is the p-value between Petal Length of versicolor and virginica 
# for samples of which Petal Length > 4


###########################################################
# correlation test
###########################################################

np.random.seed(2)
z = np.random.normal(0,1,10)
x = 1*z + np.random.normal(0,1,10)
y = 1*z + np.random.normal(0,1,10)
r = sp.stats.pearsonr(x,y)
r[0] # correlation coefficient
r[1] # p-value of correlation test
# what is the number of samples that makes p-value < 0.001

sp.stats.pearsonr(iris['Sepal.Width'],iris['Petal.Length'])

# what is the correlation and p-value between Sepal Length and Petal Width of setosa?


        
###########################################################
# chisq test
###########################################################

np.random.seed(3)
w = 1
z = np.random.normal(0,1,10)
x = w*z + np.random.normal(0,1,10)
y = w*z + np.random.normal(0,1,10)
x2 = pd.cut(x,3)
y2 = pd.cut(y,3)
tbl = pd.crosstab(x2,y2)
r = sp.stats.chisquare(tbl,axis=None)
r.pvalue
# what is the weight for p-value < 0.001?

x = pd.cut(iris['Sepal.Width'],3)
y = iris['Species']
tbl = pd.crosstab(x,y)
sp.stats.chisquare(tbl,axis=None)

# Sepal.Width와 Petal.Length 사의 correlation test의 pvalue
sp.stats.pearsonr(iris['Sepal.Width'],iris['Petal.Length'])

# Sepal.Width와 Petal.Length를 pd.cut을 이용하여 level 4개짜리 
# 범주형 데이터로 변형한 후 chi-square test를 하셔서 
# pvalue를 구하시오. 


###########################################################
# one-way anova (f-test)
###########################################################

iris1 = iris[iris['Species']=='setosa']
iris2 = iris[iris['Species']=='versicolor']
iris3 = iris[iris['Species']=='virginica']

sp.stats.f_oneway(iris1['Sepal.Length'],iris2['Sepal.Length'],iris3['Sepal.Length'])

sp.stats.f_oneway(iris1['Sepal.Length'],iris2['Sepal.Length'])
sp.stats.ttest_ind(iris1['Sepal.Length'],iris2['Sepal.Length'])




###########################################################
# Practice
###########################################################

# Practice 1
s = 0
for i in range(1,5000):
    p = xxx
    if p<0.01: s = s+1



# Practice 2



















# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

import numpy as np
import scipy as sp
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt


# Practice 1
df = pd.read_csv('data03_breastcancer.csv')
d1 = df[ df['stage']==0 ]
d2 = df[ df['stage']==1 ]
sp.stats.ttest_ind(d1['DCT'],d2['DCT'])


s = 0
for i in range(1,5000):
    v1 = d1.iloc[:,i]
    v2 = d2.iloc[:,i]
    r = sp.stats.ttest_ind(v1,v2)
    p = r.pvalue
    if p<0.01: s = s+1



# practice 2
df = pd.read_csv('data04_carseat.csv')

# case 2
plist = []
y = df['SalesBin']
for i in range(2,df.shape[1]):
    v = df.iloc[:,i]
    if type(v[0]) == type('string'): # categorical
        tbl = pd.crosstab(y,v)
        r = sp.stats.chisquare(tbl,axis=None)
    else:
        v1 = v[ y=='High' ]
        v2 = v[ y=='Low' ]
        r = sp.stats.ttest_ind(v1,v2)
    plist.append(r.pvalue)

RES = pd.DataFrame({"Name":df.columns[2:df.shape[1]], "Pvalue":plist})





















