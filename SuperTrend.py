# Importing the Libraries
import pandas as pd
import pandas_ta as ta
import json
import requests
import matplotlib.pyplot as plt


# load & store the data
url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
response = requests.get(url)
raw_data = json.loads(response.content)
data = raw_data.get("Time Series (5min)")
# print(data)


# type casting of requried fields for calculating super trend (from string to float type) 
for val in data.values():

    val['2. high'] = float(val['2. high'])
    val['3. low'] = float(val['3. low'])
    val['4. close'] = float(val['4. close'])


"""
df = pd.DataFrame(data)
print(df)
"""

# Making Dataframe
df1 = pd.DataFrame.from_dict(data, orient='index')
# print(df1)


# Super Trend Indicator
super_trend = ta.supertrend(high=df1['2. high'], low=df1['3. low'], close=df1['4. close'], period=7, multiplier=3)
# print(super_trend)

df1["6. SuperTrend"] = super_trend['SUPERT_7_3.0']
df1["7. Direction"] = super_trend['SUPERTd_7_3.0'] 
 


# Adding BuySignal and SellSignal as two Columns in our Dataframe
atr_period = 7
df1['8. BuySignal'] = 0
df1['9. SellSignal'] = 0

for i in range(atr_period, len(df1)):

    if df1['4. close'][i-1] <= df1['6. SuperTrend'][i-1] and df1['4. close'][i] > df1['6. SuperTrend'][i]:

        df1['8. BuySignal'][i] = 1

    if df1['4. close'][i-1] > df1['6. SuperTrend'][i-1] and df1['4. close'][i] <= df1['6. SuperTrend'][i]: 

        df1['9. SellSignal'][i] = 1



# Visualize the data
plt.figure(figsize=(10, 5))
plt.plot(df1['4. close'], label='Close')
plt.plot(df1['6. SuperTrend'], label='SuperTrend')
plt.title('Super Trend Indicator')
plt.ylim(149, 153)
plt.xlabel('"2021-06-11 07:05:00 to 2021-06-11 19:30:00"')
plt.ylabel('Closed Price with Super Trend Indicator')
plt.legend(loc='upper left')
plt.show()


# Show the data
print(df1)
