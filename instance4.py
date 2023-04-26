import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
from keras.models import load_model
import streamlit as st 
import yfinance as yf
from datetime import datetime

yf.pdr_override()
st.title('Stock Trend Prediction')

#my_start_date = '2010-01-01'
start_date_input = st.text_input("Enter start date (year-month-day)", '2010-01-01')
start = datetime.strptime(start_date_input, '%Y-%m-%d')

#my_end_date = '2019-12-31'
end_date_input = st.text_input("Enter end date (year-month-day)", '2019-12-31')
end = datetime.strptime(end_date_input, '%Y-%m-%d')

#Describing Data
st.subheader('data for apple')
user_input = st.text_input("Enter ticker for stock", "AAPL")
df = pdr.get_data_yahoo(user_input, start,end)
st.write(df.describe())

#visualization
st.subheader('Closing time vs Time Chart')
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig) 

#visualization for 100 Moving Average
st.subheader('Closing time vs Time Chart with 100 moving average')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig) 

#visualization for 100 moving average & 200 moving average
st.subheader('Closing time vs Time Chart with 100 moving average & 200 moving average')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)  




#Splitting  Data into Training an Testing 
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])
#print(type(data_testing))

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)

#Load my model
model = load_model('keras_model.h5')
#Testing part
past_100_days = data_training.tail(100)
#print(type(past_100_days))
#final_df = past_100_days.append(data_testing, ignore_index = True)
final_df = pd.concat([past_100_days, data_testing], ignore_index = True)
#print(type(final_df))
#final_df = past_100_days.concat(data_testing, ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test, y_test = [], []

for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i,0])
x_test,y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted*scale_factor
y_test = y_test*scale_factor

#Final predicted graph
st.subheader('Predictions vs Originals')
fig2 = plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)


