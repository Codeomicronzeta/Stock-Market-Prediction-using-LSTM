# -*- coding: utf-8 -*-
"""Time Series Analysis 1.ipynb"""

from google.colab import files
uploaded = files.upload()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('RELIANCE.BO.csv')

data.head()

data.tail()

#We have data from 5 Feb 2016 to 26 June 2020
data_close = data.reset_index()['Close']        # Taking the close column of the dataset
data_close = data_close.replace(to_replace = np.nan, value = data_close.mean())    # Replacing nan values with mean of the column

data_close.isnull().values.any()        # Checking for NaN values

plt.plot(data_close)

#LSTM are sensitive to Scale of data, we scale down values to interval (0,1)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))
data_close = scaler.fit_transform(np.array(data_close).reshape(-1,1))

data_close

# Splitting data in Test Train set
training_size = int(len(data_close) * 0.65)
test_size = len(data_close) - training_size
train_data, test_data = data_close[0 : training_size, :],data_close[training_size : len(data_close), : 1]

def  create_dataset(dataset, time_step):
  data_X, data_Y = [], []
  for i in range(len(dataset) - time_step - 1):
    a = dataset[i : (i + time_step), 0]
    data_X.append(a)
    data_Y.append(dataset[i + time_step, 0 ])
  return np.array(data_X), np.array(data_Y)

time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)



np.isnan(np.min(X_test))

np.isnan(np.min(X_test))

# Reshaping the data for LSTM
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

y_test[94] = 0.756400
y_test

X_test.shape

from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import Sequential

model = Sequential()
model.add(LSTM(50, return_sequences = True, input_shape = (100, 1)))
model.add(LSTM(50, return_sequences = True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss = 'mean_squared_error', optimizer = 'adam')

model.summary()

model.fit(X_train, y_train, validation_data = (X_test, y_test) , epochs = 100, batch_size =  64, verbose = 1 )

train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train, train_predict))

math.sqrt(mean_squared_error(y_test, test_predict))

### Plotting 
# shift train predictions for plotting
look_back=100
trainPredictPlot = np.empty_like(data_close)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict
# shift test predictions for plotting
testPredictPlot = np.empty_like(data_close)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(data_close)-1, :] = test_predict
# plot baseline and predictions
plt.plot(scaler.inverse_transform(data_close))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()

len(test_data)

x_input = test_data[288:].reshape(1,-1)
x_input.shape
temp_input = list(x_input)
temp_input = temp_input[0].tolist()

from numpy import array

lst_output=[]
n_steps=100
i=0
while(i<30):
    
    if(len(temp_input)>100):
        #print(temp_input)
        x_input=np.array(temp_input[1:])
        print("{} day input {}".format(i,x_input))
        x_input=x_input.reshape(1,-1)
        x_input = x_input.reshape((1, n_steps, 1))
        #print(x_input)
        yhat = model.predict(x_input, verbose=0)
        print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat[0].tolist())
        temp_input=temp_input[1:]
        #print(temp_input)
        lst_output.extend(yhat.tolist())
        i=i+1
    else:
        x_input = x_input.reshape((1, n_steps,1))
        yhat = model.predict(x_input, verbose=0)
        print(yhat[0])
        temp_input.extend(yhat[0].tolist())
        print(len(temp_input))
        lst_output.extend(yhat.tolist())
        i=i+1
    

print(lst_output)

day_new=np.arange(1,101)
day_pred=np.arange(101,131)

len(data_close)

plt.plot(day_new,scaler.inverse_transform(data_close[1008:]))
plt.plot(day_pred,scaler.inverse_transform(lst_output))

df3=data_close.tolist()
df3.extend(lst_output)
plt.plot(df3[1058:])

df3=scaler.inverse_transform(df3).tolist()

plt.plot(df3)

from google.colab import files
uploaded = files.upload()

data_true= pd.read_csv('RELIANCE.BO_pred.csv')

#We have data from 5 Feb 2016 to 26 July 2020
data_close_true = data_true.reset_index()['Close']        # Taking the close column of the dataset
data_close_true = data_close_true.replace(to_replace = np.nan, value = data_close_true.mean())    # Replacing nan values with mean of the column

plt.plot(df3)

plt.plot(data_close_true)

plt.figure()
plt.subplot(211)
plt.plot(df3,label = 'Predicted')
plt.subplot(212)
plt.plot(data_close_true, label = 'Actual')
plt.show()

plt.plot(data_close)
