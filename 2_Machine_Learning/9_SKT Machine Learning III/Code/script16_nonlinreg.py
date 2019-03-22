# libraries
import numpy as np
import scipy as sp
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt

# read data
df = pd.read_csv('data06_wage.csv')
X = df[['age']]
y = df['wage']
xtrain = X[df['year']<=2005]
ytrain = y[df['year']<=2005]
xtest = X[df['year']>2005]
ytest = y[df['year']>2005]

# scatter plot
f,(ax1,ax2) = plt.subplots(1,2,figsize=(8,4))
ax1.plot(xtrain['age'],ytrain,'bo')
ax2.plot(xtest['age'],ytest,'bo')
plt.show()

# linear regression
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(xtrain,ytrain)
yhat_train = lm.predict(xtrain)
yhat_test = lm.predict(xtest)

def myplot(yhat_train,yhat_test):
    f,(ax1,ax2) = plt.subplots(1,2,figsize=(8,4))
    ax1.plot(xtrain['age'],ytrain,'bo')
    tmp = pd.DataFrame({'x':xtrain['age'],'y':yhat_train}).sort_values('x')
    ax1.plot(tmp['x'],tmp['y'],'r',linewidth=2)
    ax1.set_title('Train RMSE %.2f'%np.sqrt( ((ytrain-yhat_train)**2).mean() ))
    ax2.plot(xtest['age'],ytest,'bo')
    tmp = pd.DataFrame({'x':xtest['age'],'y':yhat_test}).sort_values('x')
    ax2.plot(tmp['x'],tmp['y'],'r',linewidth=2)
    ax2.set_title('Test RMSE %.2f'%np.sqrt( ((ytest-yhat_test)**2).mean() ))

myplot(yhat_train,yhat_test)

# ploynomial regression
def genpolydat(x,d):
    vn = x.columns[0]
    x0 = x.iloc[:,0]
    for i in range(2,d+1):
        vnnew = vn+str(i)
        xnew = x0**i
        x = pd.concat([x,pd.DataFrame({vnnew:xnew})],axis=1)
    return x

# ~ age^2
xtrain2 = genpolydat(xtrain,2)
xtest2 = genpolydat(xtest,2)
lm = LinearRegression()
lm.fit(xtrain2,ytrain)
yhat_train = lm.predict(xtrain2)
yhat_test = lm.predict(xtest2)

myplot(yhat_train,yhat_test)

# ~ age^5
xtrain5 = genpolydat(xtrain,5)
xtest5 = genpolydat(xtest,5)
lm = LinearRegression()
lm.fit(xtrain5,ytrain)
yhat_train = lm.predict(xtrain5)
yhat_test = lm.predict(xtest5)

myplot(yhat_train,yhat_test)

# spline
from scipy.interpolate import UnivariateSpline
tmp = pd.DataFrame({'x':xtrain['age'],'y':ytrain}).sort_values('x')
spl = UnivariateSpline(tmp['x'],tmp['y'],s=2E6)
yhat_train = spl(xtrain['age'])
yhat_test = spl(xtest['age'])
myplot(yhat_train,yhat_test)

# lowess
import statsmodels.api as sm
l = sm.nonparametric.lowess(ytrain,xtrain['age'],frac=0.3)
from scipy.interpolate import interp1d
f = interp1d(l[:,0],l[:,1])
yhat_train = f(xtrain['age'])
yhat_test = f(xtest['age'])
myplot(yhat_train,yhat_test)

# practice
np.random.seed(1)
xtrain = 2*np.random.randn(50)
ytrain = np.exp(-xtrain**2) + 0.05*np.random.randn(50)
xtest = 2*np.random.randn(50)
ytest = np.exp(-xtest**2) + 0.05*np.random.randn(50)
# find the best regression model for the test data



























# PLEASE DO NOT GO DOWN BEFORE YOU TRY BY YOURSELF

###########################################################
# Practice Reference Code
###########################################################

# libraries
import numpy as np
import scipy as sp
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt

# data generation
np.random.seed(1)
xtrain = 2*np.random.randn(50)
ytrain = np.exp(-xtrain**2) + 0.05*np.random.randn(50)
xtest = 2*np.random.randn(50)
ytest = np.exp(-xtest**2) + 0.05*np.random.randn(50)

# ploting function
def myplot2(yhat_train,yhat_test):
    f,(ax1,ax2) = plt.subplots(1,2,figsize=(8,4))
    ax1.plot(xtrain,ytrain,'bo')
    tmp = pd.DataFrame({'x':xtrain,'y':yhat_train}).sort_values('x')
    ax1.plot(tmp['x'],tmp['y'],'r',linewidth=2)
    ax1.set_title('Train RMSE %.2f'%np.sqrt( ((ytrain-yhat_train)**2).mean() ))
    ax2.plot(xtest,ytest,'bo')
    tmp = pd.DataFrame({'x':xtest,'y':yhat_test}).sort_values('x')
    ax2.plot(tmp['x'],tmp['y'],'r',linewidth=2)
    ax2.set_title('Test RMSE %.2f'%np.sqrt( ((ytest-yhat_test)**2).mean() ))

# splice
from scipy.interpolate import UnivariateSpline
tmp = pd.DataFrame({'x':xtrain,'y':ytrain}).sort_values('x')
spl = UnivariateSpline(tmp['x'],tmp['y'],s=1)
yhat_train = spl(xtrain)
yhat_test = spl(xtest)
myplot2(yhat_train,yhat_test)




