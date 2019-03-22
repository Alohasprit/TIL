
# Pandas Module
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

# reading
data = pd.read_csv('data01_iris.csv')
data.shape
data.hist()
data.plot()
data.boxplot()

# 변수 추출
v = data['Sepal.Length']
v.shape
v.mean()
v.median()
v.var()

# 샘플 추출
idx = data['Sepal.Length']>5.8
d = data[idx]
d.shape
data[ data['Sepal.Length']>5.8 ].shape

idx = (data['Sepal.Length']>5.8) & (data['Species']=='versicolor') 
d = data[idx]

# 인덱싱
data.iloc[:5,:2]
data.iloc[-5:,:]
data.iloc[[1,3,5],[0,2,3]]
data.iloc[np.arange(0,10,2),:]

# 새로운 변수 추가
v = data['Sepal.Length']**2
data['SL2'] = v
data.shape

# 정렬
d2 = data.sort_values(by=['Sepal.Length'])
d3 = data.sort_values(by=['Sepal.Length'],ascending=False)

# 그림 그리기
x = data['Sepal.Length']
y1 = data['Petal.Length']
y2 = data['Petal.Width']
plt.plot(x,y1,'b.')
plt.plot(x,y2,'r.')





































# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt


# Practice
data = pd.read_csv('data02_college.csv')
data.shape
d_private = data[ data['Private']=='Yes' ]
d_public = data[ data['Private']=='No' ]

d_private['Expend'].mean()
d_public['Expend'].mean()

d = data.sort_values(by=['Top10perc'],ascending=False)

accrate = data['Accept']/data['Apps']
data['accrate'] = accrate
d = data.sort_values(by=['accrate'])


tmp = data[data['Private']=='Yes']
plt.plot(tmp['Outstate'],tmp['Expend'],'ro')

tmp = data[data['Private']=='No']
plt.plot(tmp['Outstate'],tmp['Expend'],'go')
plt.xlabel('Outstate')
plt.ylabel('Expend')
plt.show()




