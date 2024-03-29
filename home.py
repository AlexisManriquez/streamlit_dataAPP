import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

month ="02"
year = 2024
day = "04"
day_prev = "03"
touched = 0
touched_3 = 0
data_month = pd.DataFrame()
center_prices = []
#allow user to input month and year with a dropdown menu
month = st.text_input('Enter month', '01')
year = st.text_input('Enter year', '2024')
days = 0
#calculate # of days in the month and account for leap year
if int(month) in [1, 3, 5, 7, 8, 10, 12]:
    days = 31
elif int(month) in [4, 6, 9, 11]:
    days = 30
else:
    if int(year) % 4 == 0:
        days = 29
    else:
        days = 28
#get text file with center prices
with open(f'MATICUSDT-trades-{year}-{month}-center_prices.txt', 'r') as file:
    for line in file:
        center_prices.append(float(line.strip()))


# Load the CSV file
df_spot = pd.read_csv(f'./BTCUSDT_DATA/spot/MATICUSDT-15m-{year}-{month}/MATICUSDT-15m-{year}-{month}.csv')
df_spot.columns = ['open_time','open','high','low','close','volume','close_time',  'quote_volume', 'count', 'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore']
#df = pd.read_csv('./BTCUSDT_DATA/BTCUSDT-15m-2019-11.csv')
# Convert Unix time to datetime
df_spot['open_time'] = pd.to_datetime(df_spot['open_time'], unit='ms')
# Set the date as the index
#df_spot = df_spot.set_index('open_time')

df_spot.drop(['close_time',  'quote_volume', 'count', 'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'], axis=1, inplace=True)
#display entire dataframe
pd.set_option('display.max_rows', None)
#data = df_spot[['open_time', 'volume']]
poc_list = []
POC_hits = 0
for i in range(1, days-1):
    #extract time and volume columns
    #get rows from 2019-10-01 time 07:00:00 to 2019-10-02 time 09:00:00'
    data = pd.DataFrame()
    if i < 8:
        data = df_spot[(df_spot['open_time'] >= f'{year}-{month}-0{i+1} 09:30:00')]
    elif i == 9:
        data = df_spot[(df_spot['open_time'] >= f'{year}-{month}-{i+1} 09:30:00')]
    else:
        data = df_spot[(df_spot['open_time'] >= f'{year}-{month}-{i+1} 09:30:00')]
    data = data.set_index('open_time')
    #check if the first open price at 9:30am is greater than the center price
    if data['open'].iloc[0] > center_prices[i-1]:
            #check if the firsy price at 9:30am is greater than 3% of the center price
            if data['open'].iloc[0] > center_prices[i-1]:
                #check if the center price is touched past 9:30am for the next 7 hours
                data2 = data[data.index.hour < 17]
                if data2['low'].min() < center_prices[i-1]:
                    POC_hits += 1
    elif data['open'].iloc[0] < center_prices[i-1]:
            #check if the firsy price at 9:30am is greater than 3% of the center price
            if data['open'].iloc[0] < center_prices[i-1]:
                #check if the center price is touched past 9:30am for the next 7 hours
                data2 = data[data.index.hour < 17]
                if data2['high'].max() > center_prices[i-1]:
                    POC_hits += 1

df_spot = df_spot.set_index('open_time')
# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(
        x=df_spot.index,
        open=df_spot['open'],
        high=df_spot['high'],
        low=df_spot['low'],
        close=df_spot['close']
    )])

for i in range(1, days-1):
        if i < 8:
            x_values = pd.date_range(start=f'{year}-{month}-0{i} 19:00:00', end=f'{year}-{month}-0{i+1} 09:00:00', freq='15min')
        elif i == 9:
            x_values = pd.date_range(start=f'{year}-{month}-0{i} 19:00:00', end=f'{year}-{month}-{i+1} 09:00:00', freq='15min')
        else:
            x_values = pd.date_range(start=f'{year}-{month}-{i} 19:00:00', end=f'{year}-{month}-{i+1} 09:00:00', freq='15min')
        fig.add_trace(go.Scatter(
            x=x_values,
            y=[center_prices[i-1]] * len(x_values),
            mode='lines',
            line=dict(color='red', width=2),
            name=f'Point of Control (${center_prices[i-1]})',
        ))
        if i == days-2:
            x_values = pd.date_range(start=f'{year}-{month}-{i+1} 19:00:00', end=f'{year}-{month}-{i+2} 09:00:00', freq='15min')
            fig.add_trace(go.Scatter(
                x=x_values,
                y=[center_prices[i]] * len(x_values),
                mode='lines',
                line=dict(color='red', width=2),
                name=f'Point of Control (${center_prices[-1]})'
            ))
# hide the legend
fig.update_layout(showlegend=False)
st.title('MATICUSDT Analysis')
st.plotly_chart(fig, use_container_width=True)

# Display values from center_prices list to a nice markdown table
st.write('Center Prices')
# Create a DataFrame from the center_prices list
df_center_prices = pd.DataFrame(center_prices, columns=['Center Prices'])
# Display the DataFrame
st.dataframe(df_center_prices, use_container_width=)

