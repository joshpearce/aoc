import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import r2_score
#from sklearn.preprocessing import Normalizer

df_train = pd.read_csv('/Users/josh/Downloads/archive/train.csv')
df_test = pd.read_csv('/Users/josh/Downloads/archive/test.csv')

x_train = df_train['x']
y_train = df_train['y']
x_test = df_test['x']
y_test = df_test['y']

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)

x_train = x_train.reshape(-1,1)
x_test = x_test.reshape(-1,1)

clf = LinearRegression()
clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)
print(r2_score(y_test,y_pred))

n = 700
alpha = 0.0001

a_0 = 0
a_1 = 0

epochs = 0
while(epochs < 1000):
    y = a_0 + a_1 * x_train
    error = y - y_train
    mean_sq_er = np.sum(error**2)
    mean_sq_er = mean_sq_er/n
    a_0 = a_0 - alpha * 2 * np.sum(error)/n 
    a_1 = a_1 - alpha * 2 * np.sum(error * x_train)/n
    epochs += 1
    if(epochs%10 == 0):
        print(mean_sq_er)