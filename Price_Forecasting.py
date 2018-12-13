#%% Import package
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fbprophet import Prophet

#%% Read file
filename = 'TAIEX_200101-201812.csv'
data = pd.read_csv(filename, encoding='utf-8')
data.columns = ['日期', '開盤指數', '最高指數', '最低指數', '收盤指數']

#%% Split data
Year_Start_Train = 2001     # start year to train 
Month_Start_Train = 1       # start month to train
Year_End_Train = 2018       # end year to train
Month_End_Train = 11         # end month to train

if Year_Start_Train > Year_End_Train:
    print('Wrong Year_Start & Year_End_Train')

column_names = list(data)
for index in range(1, 4):
    data.drop(column_names[index], axis=1, inplace=True)
    
data.rename(columns = {'日期':'ds'}, inplace=True)
data.rename(columns = {'收盤指數':'y'}, inplace=True)
column_names = list(data)

for index in range(data.shape[0]):
    Date = data.iloc[index]['ds']
    Value = data.iloc[index]['y']
    Year = int(Date.split('/')[0]) + 1911
    Month = int(Date.split('/')[1])
    Day = int(Date.split('/')[2])
    data.at[index, 'ds'] =  pd.Timestamp(year=Year, month=Month, day=Day)
    data.at[index, 'y'] = float(Value.split(',')[0] + Value.split(',')[1])

split_index = 0
for index in range(data.shape[0]):
    Date = data.iloc[index]['ds']
    Year = Date.year
    Month = Date.month
    if (Year_End_Train == Year) & (Month == Month_End_Train + 1):
        split_index = index
        break
data_train = data.iloc[:split_index]
for index in range(data_train.shape[0]):
    data_train.at[index, 'y'] = np.log(data_train.loc[index, 'y'])
data_test = data.iloc[split_index:]
predict_length = (data_test.shape[0])

#%% Model training and prediction
model = Prophet(daily_seasonality=True)
model.fit(data_train)
predictor = model.make_future_dataframe(periods=predict_length)
data_prediction = model.predict(predictor)

#%% Plot result
plt.figure()
model.plot(data_prediction)

data_test.set_index('ds', inplace=True)
for index in range(data_prediction.shape[0]):
    data_prediction.at[index, 'yhat'] = np.exp(data_prediction.loc[index, 'yhat'])
data_prediction.index = list(data['ds'])
data_prediction = data_prediction.drop(['ds'], axis=1).tail(predict_length)

fig, ax1 = plt.subplots(figsize=(10, 8))
ax1.plot(data_test['y'], label='True Price')
ax1.plot(data_prediction['yhat'], 'r-', label='Predicted Price')
ax1.legend()
