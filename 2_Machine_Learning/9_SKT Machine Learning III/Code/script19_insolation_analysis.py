import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats

from sklearn.preprocessing import StandardScaler as StScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor as KNNR
from sklearn.linear_model import Lasso

from sklearn.metrics import mean_squared_error as MSE


# X Y 데이터 불러오기
# 옵션의 hour는 시간 변수 사용 여부
def load_dataSet(hour=False):
    csv_train = pd.read_csv('./data12_ins_train.csv')
    csv_test = pd.read_csv('./data13_ins_test.csv')
    column_names = csv_train.columns

    index_col = column_names.drop(['y', 'stn', 'datetime'])
    if hour == False:
        index_col = index_col.drop(['hour'])
    else:
        pass

    _trainX_raw = csv_train[index_col]
    _testX_raw = csv_test[index_col]
    _trainY_raw = csv_train['y']
    _testY_raw = csv_test['y']

    return _trainX_raw, _trainY_raw, _testX_raw, _testY_raw

# 데이터:
# 인공위성에서 지구를 빛의 파장 대에 따라 사진을 찍음. 파장 대는 총 16개 채널.
# 데이터 샘플 하나의 x는 특정 픽셀에서의 파장 대 별 수치를 기록함
# y는 일사량으로 0 ~ 4의 값을 가짐.
# 따라서 16개 변수를 가지는 x와 일사량을 나타내는 y로 구성됨

# x y train/test data 불러오기 예시
trainX_raw, trainY_raw, testX_raw, testY_raw = load_dataSet()


# 결측값 확인 (이미 정제된 데이터이므로 결측값은 없음)
def check_nan(*dataSet):
    for i in range(len(dataSet)):
        if (dataSet[i].isnull().sum().all()) == 0:
            print('..arg' + str(i + 1) + ' has no Nan value')
        else:
            print('..arg' + str(i + 1) + ' has Nan values')

# 결측값 확인 예시
check_nan(trainX_raw)
check_nan(trainX_raw, trainY_raw)


# 전체적인 Y data 분포 확인을 위한 histogram plot
def plot_Ydata(*Ydata):
    plt.close()
    # plot the distribution of each set
    for i in range(len(Ydata)):
        plt.subplot(1, len(Ydata), i + 1)
        plt.hist(Ydata[i], bins=40)

# plot 예시
plot_Ydata(trainY_raw)
plot_Ydata(trainY_raw, testY_raw)


# x y 데이터에 대해 각각 boxplot 확인
def boxplot_data_raw(_data):
    plt.close()
    if isinstance(_data, pd.DataFrame):
        columns = _data.columns
        for i in range(len(_data.columns)):
            plt.subplot(1,len(_data.columns), i+1)
            plt.boxplot(_data[columns[i]])
            plt.xticks([])
    elif isinstance(_data, pd.Series):
        plt.boxplot(_data)
        plt.xticks([])
    else:
        raise ValueError('input error')

# boxplot 확인 예시
boxplot_data_raw(trainX_raw)
boxplot_data_raw(trainY_raw)

# 관측 데이터(y 값)의 분포를 볼 때 0에 가까운 값이 상당히 많음. 일사량 예측에 크게 중요하지 않은 데이터이므로 sampling하여 제거
# 옵션 th : down sampling 할 y 값의 threshold 값.
# 옵션 frac : 제거(drop)할 비율
def trim_data(_trainX_raw, _trainY_raw, th = 0.1, frac = 0.9):
    # trim out data where y < 0.1
    index_toDrop = _trainY_raw[_trainY_raw < th].sample(frac=frac).index
    _trainX_trim = _trainX_raw.drop(index_toDrop)
    _trainY_trim = _trainY_raw.drop(index_toDrop)

    return _trainX_trim, _trainY_trim

# 0 값 downsampling 예시
trainX_trim, trainY_trim = trim_data(trainX_raw, trainY_raw, 0.1, 0.9)

# X data의 각 변수 별 분포 plot을 확인했을 때 전체적으로 편향되어 있으므로 log scaling 시행
# 7번 째 변수는 반대방향으로 skewed 되어있으므로 관측 최고 파장대인 x= 17000 선대칭 후 logscaling
def handle_skewed_X(_trainX_trim, _testX_raw):
    # handle skewed data
    for i in range(1, 17):
        ch = 'ch' + str(i)
        if i == 7:
            _trainX_trim[ch] = (17000 - _trainX_trim[ch]).apply(np.log)
            _testX_raw[ch] = (17000 - _testX_raw[ch]).apply(np.log)
        else:
            _trainX_trim[ch] = _trainX_trim[ch].apply(np.log)
            _testX_raw[ch] = _testX_raw[ch].apply(np.log)

    return _trainX_trim, _testX_raw


trainX_ctr, testX_ctr = handle_skewed_X(trainX_trim, testX_raw)

# 학습 전에 X 입력변수들을 각각 Standardization 진행
scalerX = StScaler().fit(trainX_ctr)
trainX_scale = pd.DataFrame(scalerX.transform(trainX_ctr), columns=trainX_ctr.columns)
testX_scale = pd.DataFrame(scalerX.transform(testX_ctr), columns=testX_ctr.columns)

# Y 값은 MinMax Scaling을 하며, 관측가능한 최대/최저값이 각각 0,4 이므로 4로 나누어줌
trainY_scale = trainY_trim / 4

# 전처리 전 후 y 데이터 비교 plot 함수
def plot_trimmed_Ydata(_trainY_raw, _trainY_trim):
    plt.close()
    plt.subplot(1, 2, 1)
    plt.hist(_trainY_raw, bins=40)
    plt.subplot(1, 2, 2)
    plt.hist(_trainY_trim, bins=40)

plot_trimmed_Ydata(trainY_raw,trainY_scale)

# 전처리 전 후 x 데이터 비교 plot 함수
def plot_trimmed_Xdata(_trainX_raw, _trainX_trim):
    plt.close()
    n = _trainX_raw.shape[1]
    for i in range(n):
        ch = 'ch' + str(i)
        plt.subplot(2, n, i+1);
        plt.xticks([]);
        plt.yticks([])
        plt.hist(_trainX_raw.iloc[:,i], bins=40)
        plt.subplot(2, n, n + i+1)
        plt.hist(_trainX_trim.iloc[:,i], bins=40);
        plt.xticks([]);
        plt.yticks([])

plot_trimmed_Xdata(trainX_raw.iloc[:,:2],trainX_ctr.iloc[:,:2])


# x 변수 간 correlation 확인 위한 히트맵
def plot_heatmap(_trainX_scale):
    # heatmap
    plt.close()
    corr_mat = _trainX_scale.corr()
    sns.heatmap(corr_mat)

plot_heatmap(trainX_scale)

# x 변수 간 correlation 확인 위한 pairplot
def plot_pairplot(_trainX_scale):
    plt.close()
    # 변수를 많이 넣을 시 컴퓨터 사양에 따라 성능 저하될 수 있음
    sns.pairplot(_trainX_scale[['ch1', 'ch2']])

# PCA 필요한 경우
# pca = PCA(n_components=4)
# pca.fit(trainX_scale)
# trainX_pca = pca.transform(trainX_scale)

# regressor 예시
# 모델 별로 _param_grid 설정하여 model selection 진행
# _param_grid 는 dictionary 형태로 각 regression 모델의 parameter변수를 설정. parameter의 range마다 cross validation을 하여 최적의 parameter값을 찾음
# _param_grid 의 CV와 parameter 튜닝을 같이 하므로 학습시간이 길기 때문에 parameter의 range는 적게 설정해서 테스트. 아래는 예시
def regressor(model='RFR', _param_grid = None):
    if model == 'RFR':
        _regr = RFR()
        if _param_grid == None:
            _param_grid = {'n_estimators': [100, 200], 'min_samples_leaf': [0.001, 0.0005], 'max_features': [0.3]}
        else:
            pass
    elif model == 'KNNR':
        _regr = KNNR()
        if _param_grid == None:
            _param_grid = {'n_neighbors': [3, 5]}
        else:
            pass
    else:
        raise ValueError('no such a regressor ...')

    return _regr, _param_grid


# regressor 선택
regr, param_grid = regressor('RFR')

# n fold tuning
n_fold_cv = 3

# cross validation를 통한 model selection 세팅
grid = GridSearchCV(regr, param_grid=param_grid, cv=n_fold_cv, return_train_score=True)

# 학습 진행
grid.fit(trainX_scale, trainY_scale)

# best parameter 표시
print(grid.best_params_)

# best estimator 리턴
optimised_model = grid.best_estimator_

# test set 성능 테스트
predY_scale = optimised_model.predict(testX_scale)

MSE(testY_raw, predY_scale * 4)
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(testY_raw, predY_scale * 4)
print(r_value**2)

# scatter plot 확인
plt.scatter(testY_raw, predY_scale * 4)


####################################################################
# Practice
####################################################################

# Ridge, Lasso, SVR 혹은 다른 방식을 이용하여 insolation을 예측하고,
# 그 성능을 측정하시오. 





































####################################################################
# Practice Reference Code
####################################################################

def regressor(model='RFR', _param_grid = None):
    if model == 'RFR':
        _regr = RFR()
        if _param_grid == None:
            _param_grid = {'n_estimators': [100, 200], 'min_samples_leaf': [0.001, 0.0005], 'max_features': [0.3]}
        else:
            pass
    elif model == 'SVR':
        _regr = SVR()
        if _param_grid == None:
            _param_grid = {'C': [0.1, 1], 'kernel': ['rbf', 'linear'], 'gamma': [0.1, 1]}
        else:
            pass
    elif model == 'KNNR':
        _regr = KNNR()
        if _param_grid == None:
            _param_grid = {'n_neighbors': [3, 5]}
        else:
            pass
    elif model == 'Lasso':
        _regr = Lasso()
        if _param_grid == None:
            _param_grid = {'alpha': [0.1, 1]}
        else:
            pass
    elif model == 'Ridge':
        _regr = Ridge()
        if _param_grid == None:
            _param_grid = {'alpha': [0.1, 1]}
        else:
            pass
    else:
        raise ValueError('no such a regressor ...')

    return _regr, _param_grid
