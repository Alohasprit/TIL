# libraries
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# read data
df = pd.read_csv('data01_iris.csv')
X = df[ ['Sepal.Length','Sepal.Width','Petal.Length','Petal.Width'] ]


###########################################################
# KMeans
###########################################################
# kmeans
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)
km.fit(X)
km.labels_
pd.crosstab(km.labels_,df['Species'])

# clustering with selected variables
km.fit(X.iloc[:,[0,1]])
pd.crosstab(km.labels_,df['Species'])
# what is the best subset for the clustering?

# pca & clustering
from sklearn.decomposition import PCA
pca = PCA()
xtrans = pca.fit_transform(X)
km = KMeans(n_clusters=3)
km.fit(xtrans[:,(0,1)])
pd.crosstab(km.labels_,df['Species'])

# scaling, pca, clustering
from sklearn.preprocessing import scale
xscaled = scale(X,axis=0,with_mean=True,with_std=True)
km.fit(xscaled)
pd.crosstab(km.labels_,df['Species'])

x = pca.fit_transform(xscaled)
km.fit(x[:,(0,1)])
pd.crosstab(km.labels_,df['Species'])

###########################################################
# Hierachical clustering
###########################################################

from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters=3)
hc.fit(X)
pd.crosstab(hc.labels_,df['Species'])
hc.children_

# different options
hc = AgglomerativeClustering(n_clusters=3,affinity='cosine',linkage='complete')
hc.fit(X)
pd.crosstab(hc.labels_,df['Species'])


###########################################################
# Practice 
###########################################################

df = pd.read_csv('data02_college.csv')
X = df.iloc[:,2:]
Y = df['Private']








































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# practice
df = pd.read_csv('data02_college.csv')
X = df.iloc[:,2:]
Y = df['Private']

# Kmeans
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)
km.fit(X)
pd.crosstab(km.labels_,Y)

# scaling
from sklearn.preprocessing import scale
xscaled = scale(X,axis=0,with_mean=True,with_std=True)
km = KMeans(n_clusters=3)
km.fit(xscaled)
pd.crosstab(km.labels_,Y)

# pca
from sklearn.decomposition import PCA
pca = PCA()
xtrans = pca.fit_transform(xscaled)
km.fit(xtrans[:,:2])
pd.crosstab(km.labels_,Y)

