# libraries
import numpy as np
import scipy as sp
import pandas as pd

# read data
df = pd.read_csv('data07_diabetes.csv')
X = df.iloc[:,:-1]
y = df['Y']

# boston data set
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.75,random_state=0)

# forward feature selection
np.random.seed(0)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
vn = list(xtrain.columns)
f_sel= []
score = []
for i in range(xtrain.shape[1]):
    s = np.zeros(len(vn))
    for j in range(len(vn)):
        v = f_sel.copy()
        v.append(vn[j])
        x = xtrain[v]
        f = LinearRegression()
        cv_score = cross_val_score(f,x,ytrain,cv=5)
        s[j] = cv_score.mean()
    v = vn[s.argmax()]
    f_sel.append(v)
    vn.remove(v)
    score.append(s.max())
    print("%02d Selected:"%i,f_sel)
    print("%02d Score   :"%i,np.round(10000*np.array(score))/10000)

# finally selected features    
f_sel_final = f_sel[:(np.array(score).argmax()+1)]

# test on the test set
from sklearn.linear_model import LinearRegression
f = LinearRegression()
f.fit(xtrain[f_sel_final],ytrain)
f.score(xtest[f_sel_final],ytest)

# comparison with the full model
f.fit(xtrain,ytrain)
f.score(xtest,ytest)




###########################################################
# Practice
###########################################################

# practice 1
# implement backward feature selection and test over the diabetes data set

# practice 2
df = pd.read_csv('data02_college.csv')
X = df.iloc[:,3:]
y = df['Accept']/df['Apps']
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.75,random_state=1)
# find the best model using feature selection methods

























# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# practice 1

# libraries
import numpy as np
import scipy as sp
import pandas as pd

# read data
df = pd.read_csv('data05_diabetes.csv')
X = df.iloc[:,:-1]
Y = df['Y']

# boston data set
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.75,random_state=0)

# backward feature selection
np.random.seed(0)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
vn = list(xtrain.columns)
f_sel_list = []
score = []
for i in range(xtrain.shape[1]):
    if i == 0: # full model
        x = xtrain
        f = LinearRegression()
        f.fit(x,ytrain)
        s = cross_val_score(f,x,ytrain,cv=5).mean()
    else: 
        s = np.zeros(len(vn))
        for j in range(len(vn)):
            v = vn.copy()
            v.remove(vn[j])
            x = xtrain[v]
            f = LinearRegression()
            f.fit(x,ytrain)
            s[j] = cross_val_score(f,x,ytrain,cv=5).mean()        
        v = vn[s.argmax()]
        vn.remove(v)
    f_sel_list.append(vn.copy())
    score.append(s.max())
    print("%02d Selected:"%i,vn)
    print("%02d Score   :"%i,np.round(10000*np.array(score))/10000)


# finally selected features    
f_sel_final = f_sel_list[np.array(score).argmax()]

# test on the test set
from sklearn.linear_model import LinearRegression
f = LinearRegression()
f.fit(xtrain[f_sel_final],ytrain)
f.score(xtest[f_sel_final],ytest)

# comparison with the full model
f.fit(xtrain,ytrain)
f.score(xtest,ytest)


# practice 2
df = pd.read_csv('data02_college.csv')
X = df.iloc[:,3:]
y = df['Accept']/df['Apps']
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.75,random_state=1)

# forward feature selection
np.random.seed(0)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
vn = list(xtrain.columns)
f_sel= []
score = []
for i in range(xtrain.shape[1]):
    s = np.zeros(len(vn))
    for j in range(len(vn)):
        v = f_sel.copy()
        v.append(vn[j])
        x = xtrain[v]
        f = LinearRegression()
        cv_score = cross_val_score(f,x,ytrain,cv=5)
        s[j] = cv_score.mean()
    v = vn[s.argmax()]
    f_sel.append(v)
    vn.remove(v)
    score.append(s.max())
    print("%02d Selected:"%i,f_sel)
    print("%02d Score   :"%i,np.round(10000*np.array(score))/10000)

# finally selected features    
f_sel_final = f_sel[:(np.array(score).argmax()+1)]

# test on the test set
from sklearn.linear_model import LinearRegression
f = LinearRegression()
f.fit(xtrain[f_sel_final],ytrain)
f.score(xtest[f_sel_final],ytest)

# comparison with the full model
f.fit(xtrain,ytrain)
f.score(xtest,ytest)


