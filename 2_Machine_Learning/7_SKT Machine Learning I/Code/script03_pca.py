# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# read data
df = pd.read_csv('data01_iris.csv')
xorg = df[ ['Sepal.Length','Sepal.Width','Petal.Length','Petal.Width'] ]

# PCA 
from sklearn.decomposition import PCA
pca = PCA()
xtrans = pca.fit_transform(xorg)
xorg.var(axis=0)
xorg.var(axis=0)/sum(xorg.var(axis=0))
pca.explained_variance_
pca.explained_variance_ratio_

# PCA with scaling
from sklearn.preprocessing import scale
xscaled = scale(xorg)
pca = PCA()
xtrans = pca.fit_transform(xscaled)
xscaled.var(axis=0)
xscaled.var(axis=0)/sum(xscaled.var(axis=0))
pca.explained_variance_
pca.explained_variance_ratio_

# Reconstruction
xrecon = pca.inverse_transform(xtrans)
e = (xscaled-xrecon)**2
e.mean()

pca1 = PCA(n_components=1)
xtrans1 = pca1.fit_transform(xscaled)
xrecon = pca1.inverse_transform(xtrans1)
e = (xscaled-xrecon)**2
e.mean()

# Train/Test in PCA
from sklearn.model_selection import train_test_split
xtrain, xtest = train_test_split(xorg,test_size=0.4,random_state=0) 

pca = PCA()
xtrans_train = pca.fit_transform(xtrain)
xtrans_test = pca.transform(xtest)



###########################################################
# Practice 
###########################################################

df = pd.read_csv('data02_college.csv')
x = df.iloc[:,2:]
# (1) 전체 variance 중 몇 %를 처음 2개의 PC가 설명하는가?
# (2) 90% 이상의 variance를 설명하려면 몇 개의 PC가 필요한가?
# (3) 스케일링 후에 (1)과 (2)를 반복하시오.
# (4) 첫 번 째와 두 번 째 PC를 plot하고, 무엇을 관찰할 수 있는지 생각하시오.
# (5) 스케일링 없이 PCA를 수행 후, 처음의 두 PC로 원래 데이터를 재구성하시오.
#    이 때, 재구성 에러는 얼마인가?





























# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# practice
df = pd.read_csv('data02_college.csv')
x = df.iloc[:,2:]

pca = PCA()
xtrans = pca.fit_transform(x)
pca.explained_variance_ratio_
pca.explained_variance_ratio_.cumsum()
 
