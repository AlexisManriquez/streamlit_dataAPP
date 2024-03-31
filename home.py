import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from lightweight_charts.widgets import StreamlitChart
if __name__ == '__main__':
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

    df_copy = df_spot.copy()
    #rename open_time column to time
    df_copy.rename(columns={'open_time': 'time'}, inplace=True)
    df_spot = df_spot.set_index('open_time')
    st.title('MATICUSDT Analysis')
    chart = StreamlitChart(width=900, height=600,toolbox=True)
    chart.set(df_copy)
    chart.precision(4)
    for i in range(1, days-1):
            POC_list = []
            if i < 8:
                x_values = pd.date_range(start=f'{year}-{month}-0{i} 19:00:00', end=f'{year}-{month}-0{i+1} 09:00:00', freq='15min')
            elif i == 9:
                x_values = pd.date_range(start=f'{year}-{month}-0{i} 19:00:00', end=f'{year}-{month}-{i+1} 09:00:00', freq='15min')
            else:
                x_values = pd.date_range(start=f'{year}-{month}-{i} 19:00:00', end=f'{year}-{month}-{i+1} 09:00:00', freq='15min')
            POC_list.extend([[row, center_prices[i-1]] for row in x_values])
            POC_df = pd.DataFrame(POC_list, columns=['time', f'{year}-{month}-{i+1} POC'])
            line = chart.create_line(name=f'{year}-{month}-{i+1} POC', color='red', price_label=False, price_line=False)
            line.set(POC_df)
            if i == days-2:
                POC_list = []
                x_values = pd.date_range(start=f'{year}-{month}-{i+1} 19:00:00', end=f'{year}-{month}-{i+2} 09:00:00', freq='15min')
                POC_list.extend([[row, center_prices[-1]] for row in x_values])
                POC_df = pd.DataFrame(POC_list, columns=['time', f'{year}-{month}-{i+2} POC'])
                line = chart.create_line(name=f'{year}-{month}-{i+2} POC', color='red', price_label=False, price_line=False)
                line.set(POC_df)
    chart.load()