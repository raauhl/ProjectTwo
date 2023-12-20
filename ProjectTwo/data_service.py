import requests
import key_info

from enumerations import Function 
from enumerations import OutputSize
from enumerations import Candle

import file_service
import constants

import pandas as pd

import data_service_helper

base_url = 'https://www.alphavantage.co/query?'


def get_data(function, symbol, outputsize, key):

    url = base_url + 'function={function}&symbol={symbol}&outputsize={outputsize}&apikey={apikey}'.format(
        function=function,
        symbol=symbol,
        outputsize=outputsize,
        apikey=key,
    )

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        file_service.create(data_json_blob=data, file_path=symbol+'_'+outputsize+'.json')
        return data
    else:
        print("Request failed with status code:", response.status_code)
        return None
    


def baseline():

    data = file_service.read('IVE_full.json')
    time_series = data[constants.TIME_SERIES_DAILY]
    
    time_series = list(time_series.items())
    date_1, values_1 = time_series[0]
    date_2, values_2 = time_series[-1]

    cost_price = float(values_2[Candle.CLOSE])
    sell_price = float(values_1[Candle.CLOSE])
    years = int(date_1[:4]) - int(date_2[:4])

    print(cost_price, sell_price, years)
    cagr = data_service_helper.calculate_cagr(cost_price, sell_price, years)
    print("CAGR: ", cagr)
    return cagr
    

def process_one():

    # when we buy at open and sell at close

    def percentage_diff(initial_val, final_value):
        initial_val, final_value = float(initial_val), float(final_value)
        return ((final_value - initial_val) / initial_val) * 100

    data = file_service.read('IVE_full.json')
    time_series = data[constants.TIME_SERIES_DAILY]

    positive_days = negative_days = neutral_days = 0
    positive_sum = negative_sum = 0
    data_series = []
    
    for date, values in time_series.items():
        open_price = values[Candle.OPEN]
        high_price = values[Candle.HIGH]
        low_price = values[Candle.LOW]
        close_price = values[Candle.CLOSE]
        candle = [open_price, high_price, low_price, close_price]
        data_series.append(candle)

    for i in range(len(data_series)):
        open_price, high_price, low_price, close_price = data_series[i]
        percentage_diff_today = percentage_diff(open_price, close_price)

        if close_price > open_price:
            positive_sum += percentage_diff_today
            positive_days += 1
        elif close_price < open_price:
            negative_sum += percentage_diff_today
            negative_days += 1
        else:
            neutral_days += 1
    
    print(positive_days, negative_days, neutral_days)
    print(positive_sum / positive_days, negative_sum / negative_days)
    print(len(time_series.items()))

def process_two():

    data = file_service.read('IVE_full.json')
    time_series = data[constants.TIME_SERIES_DAILY]

    ohlc_data = []

    for date, values in time_series.items():
        ohlc_data.append({
            'date': date,
            'open': float(values[Candle.OPEN]),
            'high': float(values[Candle.HIGH]),
            'low': float(values[Candle.LOW]),
            'close': float(values[Candle.CLOSE]),
            'volume': int(values[Candle.VOLUME])
        })

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(ohlc_data)

    # df['date'] = pd.to_datetime(df['date'])
    # df.set_index('date', inplace=True)
    # moving_average = df['close'].rolling(window=50).mean()
    # print(moving_average.head(100))

    

data = get_data(Function.TIME_SERIES_DAILY_ADJUSTED, 'SPX', OutputSize.FULL, key_info.api_key)
# process_one()
# process_two()
baseline()

