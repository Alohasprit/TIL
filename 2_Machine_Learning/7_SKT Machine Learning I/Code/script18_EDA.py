# libraries
import numpy as np
import scipy as sp
import pandas as pd


###########################################################
# EDA
###########################################################

df = pd.read_csv('data01_iris.csv')
df.head()
df.describe(include='all')
df['Species'].value_counts()
df.hist()
df.plot()
df.boxplot()

###########################################################
# Outlier Detection
###########################################################

# univariate outlier detection
# outlier check for each variable
df[['Sepal.Length']].boxplot()

# multivariate outlier detection
x = df.iloc[:,:-1].values
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)
km.fit(x)
center_matrix = km.cluster_centers_[km.labels_,:]
dist = ((x-center_matrix)**2).sum(axis=1)
np.sort(dist)
outlier_idx = dist>2.0

# using sophisticated functions
from sklearn.neighbors import LocalOutlierFactor
f = LocalOutlierFactor()
detect = f.fit_predict(x)
outlier_idx2 = detect==-1
pd.crosstab(outlier_idx,outlier_idx2)


###########################################################
# Missing Value Imputation 
###########################################################

df = pd.read_csv('data11_khan2.csv')
xorg = df.values

# missing value detection
naidx = np.isnan(xorg)
naidx.sum()
naidx.sum(axis=0)
naidx.sum(axis=1)
xorg[naidx]

# simple missing value imputation
from sklearn.impute import SimpleImputer

f = SimpleImputer(missing_values=np.nan,strategy='mean')
xfill = f.fit_transform(xorg)
np.isnan(xfill).sum().sum()
xfill[naidx]

f = SimpleImputer(missing_values=np.nan,strategy='constant',fill_value=0)
xfill = f.fit_transform(xorg)
xfill[naidx]


###########################################################
# Practice 
###########################################################

# iris3은 iris 데이터 셋에 임의로 이상치를 넣어 생성한 데이터이다. 
# (1) iris3을 읽어 이상치를 검출하시오. 몇 개의 이상치가 검출되었는가?
#    이를 원래 iris데이터와 비교하였을 때, 얼마나 올바르게 검출되었나?
# (2) Univariate 방법을 이용하여 이상치를 결측처리하고, 이를 추정하시오.
#    추정된 값과 원래 iris데이터의 값을 비교하였을 때, 추정에러를 구하시오. 
xorg = pd.read_csv('data01_iris.csv').iloc[:,:-1].values
xout = pd.read_csv('data10_iris3.csv').iloc[:,:-1].values
outlier_idx_true = (xorg!=xout)











































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# read data
xorg = pd.read_csv('data01_iris.csv').iloc[:,:-1].values
x = pd.read_csv('data10_iris3.csv').iloc[:,:-1].values
outlier_idx_true = (xorg!=x)
((xorg-x)**2).mean()

# (1) outlier detection
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)
km.fit(x)
center_matrix = km.cluster_centers_[km.labels_,:]
dist = ((x-center_matrix)**2).sum(axis=1)
np.sort(dist)
pd.DataFrame({"dist":dist}).boxplot()
outlier_idx = dist>20
pd.crosstab(outlier_idx,outlier_idx_true.sum(axis=1)>0)

# (2) Missing value imputation
pd.DataFrame({"x":x[:,2]}).boxplot()
idx = (x[:,0]<3) | (x[:,0]>8)
x[idx,0] = np.nan

for i in range(1,4):
    v = x[:,i]
    p25 = np.percentile(v,25)
    p75 = np.percentile(v,75)
    lower = p25-1.5*(p75-p25)
    upper = p75+1.5*(p75-p25)
    idx = (v<lower) | (v>upper)
    x[idx,i] = np.nan

naidx = np.isnan(x)
pd.crosstab(naidx.reshape((600,)),outlier_idx_true.reshape((600,)))

from sklearn.impute import SimpleImputer
f = SimpleImputer(missing_values=np.nan,strategy='mean')
xfill = f.fit_transform(x)
np.isnan(xfill).sum().sum()
xfill[naidx]
((xorg-xfill)**2).mean()


