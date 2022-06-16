import sys
import time

from alpaca_trade_api import REST, TimeFrame
from sklearn import svm
from sklearn.neural_network import MLPClassifier, MLPRegressor

import keys
from datetime import datetime, timedelta
from talib._ta_lib import *
import pandas as pd
import numpy as np


def main():
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    # clock = api.get_clock()
    # timestamp = clock.timestamp
    # # print(timestamp)
    # format1 = "%Y-%m-%d %H:%M:%S.%f"
    # dt = datetime.strptime(str(timestamp)[:-9], format1)
    # # print(dt)
    # delta1 = timedelta(days=1)
    # delta2 = timedelta(days=1) + delta1
    #
    # format2 = "%Y-%m-%dT%H:%M:%S-05:00"  # dependent on UTC-5
    # start = ((dt - delta2).strftime(format2))
    # end = ((dt - delta1).strftime(format2))
    # print(start)
    # print(end)

    start = '2018-01-01T10:00:00-05:00'
    format2 = "%Y-%m-%dT%H:%M:%S-05:00"
    current_timestamp = datetime.strptime(start, format2)

    X = []
    y = []

    # give it current_time minus 1 day up to current_timestamp plus 6 hours, where last item (if not weekend) is desired close price

    for i in range(1000):     # train
        time.sleep(0.5)
        # print(current_timestamp)
        bars = api.get_bars("AAPL", TimeFrame.Minute, (current_timestamp - timedelta(days=1)).strftime(format2),
                            (current_timestamp + timedelta(hours=6)).strftime(format2), adjustment='raw').df
        # print(bars)

        if len(bars) > 1088:

            high = bars['high']
            # continue
            low = bars['low']
            open = bars['open']
            close = bars['close']
            volume = bars['volume']

            # ALL Momentum Indicators:
            bars['ADX'] = ADX(high, low, close, timeperiod=14)
            bars['ADXR'] = ADXR(high, low, close, timeperiod=14)
            bars['APO'] = APO(close, fastperiod=12, slowperiod=26, matype=0)
            bars['AROONDOWN'], bars['AROONUP'] = AROON(high, low, timeperiod=14)
            bars['AROONSC'] = AROONOSC(high, low, timeperiod=14)
            bars['BOP'] = BOP(open, high, low, close)
            bars['CCI'] = CCI(high, low, close, timeperiod=14)
            bars['CMO'] = CMO(close, timeperiod=14)
            bars['DX'] = DX(high, low, close, timeperiod=14)
            bars['MACD'], bars['MACDSIGNAL'], bars['MACDHIST'] = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
            bars['MACDEXT'], bars['MACDSIGNALEXT'], bars['MACDHISTEXT'] = MACDEXT(close, fastperiod=12, fastmatype=0,
                                                                                  slowperiod=26, slowmatype=0,
                                                                                  signalperiod=9, signalmatype=0)
            bars['MACDFIX'], bars['MACDSIGNALFIX'], bars['MACDHISTFIX'] = MACDFIX(close, signalperiod=9)
            bars['MFI'] = MFI(high, low, close, volume, timeperiod=14)
            bars['MINUS_DI'] = MINUS_DI(high, low, close, timeperiod=14)
            bars['MINUS_DM'] = MINUS_DM(high, low, timeperiod=14)
            bars['MOM'] = MOM(close, timeperiod=10)
            bars['PLUS_DI'] = PLUS_DI(high, low, close, timeperiod=14)
            bars['PLUS_DM'] = PLUS_DM(high, low, timeperiod=14)
            bars['PPO'] = PPO(close, fastperiod=12, slowperiod=26, matype=0)
            bars['ROC'] = ROC(close, timeperiod=10)
            bars['ROCP'] = ROCP(close, timeperiod=10)
            bars['ROCR'] = ROCR(close, timeperiod=10)
            bars['ROCR100'] = ROCR100(close, timeperiod=10)
            bars['RSI'] = RSI(close, timeperiod=14)
            bars['SLOWK'], bars['SLOWD'] = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0,
                                                 slowd_period=3,
                                                 slowd_matype=0)
            bars['FASTK'], bars['FASTD'] = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
            bars['FASTKSRI'], bars['FASTDSRI'] = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
            bars['TRIX'] = TRIX(close, timeperiod=30)
            bars['ULTOSC'] = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
            bars['WILLR'] = WILLR(high, low, close, timeperiod=14)

            bars = bars[88:]    # TRIX has 88 NaN values first (the most)

            try:
                day_x = bars[len(bars)-1000:]
                start_price = bars.loc[bars.index == current_timestamp.strftime(format2)]['close'][0]
                end_price = bars.loc[bars.index == (current_timestamp + timedelta(hours=6)).strftime(format2)]['close'][0]
                day_y = end_price > start_price
                X.append(day_x)
                y.append(day_y)
                print("added training day", i)
            except:
                print("error")

        current_timestamp += timedelta(days=1)

    # sys.exit(0)

    svr = MLPRegressor()    # MLPRegressor or MLPClassifier

    X = np.array(X)
    # print(X)
    y = np.array(y)
    # print(X.shape)
    nsamples, nx, ny = X.shape
    # print(X.shape)
    X = X.reshape((nsamples, nx * ny))
    # print(X.shape)
    # print(X.ndim)
    # print(y.ndim)
    # print(X)
    svr.fit(X, y)

    for i in range(100):     # test
        time.sleep(0.5)
        bars = api.get_bars("AAPL", TimeFrame.Minute, (current_timestamp - timedelta(days=1)).strftime(format2),
                            (current_timestamp + timedelta(hours=6)).strftime(format2), adjustment='raw').df

        if len(bars) > 1088:

            high = bars['high']
            # continue
            low = bars['low']
            open = bars['open']
            close = bars['close']
            volume = bars['volume']

            # ALL Momentum Indicators:
            bars['ADX'] = ADX(high, low, close, timeperiod=14)
            bars['ADXR'] = ADXR(high, low, close, timeperiod=14)
            bars['APO'] = APO(close, fastperiod=12, slowperiod=26, matype=0)
            bars['AROONDOWN'], bars['AROONUP'] = AROON(high, low, timeperiod=14)
            bars['AROONSC'] = AROONOSC(high, low, timeperiod=14)
            bars['BOP'] = BOP(open, high, low, close)
            bars['CCI'] = CCI(high, low, close, timeperiod=14)
            bars['CMO'] = CMO(close, timeperiod=14)
            bars['DX'] = DX(high, low, close, timeperiod=14)
            bars['MACD'], bars['MACDSIGNAL'], bars['MACDHIST'] = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
            bars['MACDEXT'], bars['MACDSIGNALEXT'], bars['MACDHISTEXT'] = MACDEXT(close, fastperiod=12, fastmatype=0,
                                                                                  slowperiod=26, slowmatype=0,
                                                                                  signalperiod=9, signalmatype=0)
            bars['MACDFIX'], bars['MACDSIGNALFIX'], bars['MACDHISTFIX'] = MACDFIX(close, signalperiod=9)
            bars['MFI'] = MFI(high, low, close, volume, timeperiod=14)
            bars['MINUS_DI'] = MINUS_DI(high, low, close, timeperiod=14)
            bars['MINUS_DM'] = MINUS_DM(high, low, timeperiod=14)
            bars['MOM'] = MOM(close, timeperiod=10)
            bars['PLUS_DI'] = PLUS_DI(high, low, close, timeperiod=14)
            bars['PLUS_DM'] = PLUS_DM(high, low, timeperiod=14)
            bars['PPO'] = PPO(close, fastperiod=12, slowperiod=26, matype=0)
            bars['ROC'] = ROC(close, timeperiod=10)
            bars['ROCP'] = ROCP(close, timeperiod=10)
            bars['ROCR'] = ROCR(close, timeperiod=10)
            bars['ROCR100'] = ROCR100(close, timeperiod=10)
            bars['RSI'] = RSI(close, timeperiod=14)
            bars['SLOWK'], bars['SLOWD'] = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0,
                                                 slowd_period=3,
                                                 slowd_matype=0)
            bars['FASTK'], bars['FASTD'] = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
            bars['FASTKSRI'], bars['FASTDSRI'] = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3,
                                                          fastd_matype=0)
            bars['TRIX'] = TRIX(close, timeperiod=30)
            bars['ULTOSC'] = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
            bars['WILLR'] = WILLR(high, low, close, timeperiod=14)

            bars = bars[88:]  # TRIX has 88 NaN values first (the most)


            try:
                day_x = bars[len(bars)-1000:]
                day_x = np.array(day_x)
                day_x = day_x.reshape((1, nx * ny))
                # print(day_x.shape)
                # nx, ny = day_x.shape

                prediction = (svr.predict(day_x) > 0.5)[0]
                start_price = bars.loc[bars.index == current_timestamp.strftime(format2)]['close'][0]
                end_price = bars.loc[bars.index == (current_timestamp + timedelta(hours=6)).strftime(format2)]['close'][0]
                day_y = end_price > start_price
                # print(prediction)
                # print(end_price)
                # print(start_price)
                # print(day_y)
                print(prediction == day_y, i)
            except:
                print("error")

        current_timestamp += timedelta(days=1)



    # bars = api.get_bars("AAPL", TimeFrame.Minute, start, end, adjustment='raw').df
    # # print(bars)
    # timestamps = bars.index.tolist()
    # new_timestamps = []
    # for t in timestamps:
    #     new_timestamps.append(int(t.timestamp()))
    # bars['new_timestamps'] = new_timestamps
    #
    # high = bars['high']
    # low = bars['low']
    # open = bars['open']
    # close = bars['close']
    # volume = bars['volume']
    #
    # # bars['30_Day_SMA'] = ta.SMA(bars['close'], timeperiod=30)
    # # ALL Momentum Indicators:
    # bars['ADX'] = ADX(high, low, close, timeperiod=14)
    # bars['ADXR'] = ADXR(high, low, close, timeperiod=14)
    # bars['APO'] = APO(close, fastperiod=12, slowperiod=26, matype=0)
    # bars['AROONDOWN'], bars['AROONUP'] = AROON(high, low, timeperiod=14)
    # bars['AROONSC'] = AROONOSC(high, low, timeperiod=14)
    # bars['BOP'] = BOP(open, high, low, close)
    # bars['CCI'] = CCI(high, low, close, timeperiod=14)
    # bars['CMO'] = CMO(close, timeperiod=14)
    # bars['DX'] = DX(high, low, close, timeperiod=14)
    # bars['MACD'], bars['MACDSIGNAL'], bars['MACDHIST'] = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    # bars['MACDEXT'], bars['MACDSIGNALEXT'], bars['MACDHISTEXT'] = MACDEXT(close, fastperiod=12, fastmatype=0,
    #                                                                       slowperiod=26, slowmatype=0,
    #                                                                       signalperiod=9, signalmatype=0)
    # bars['MACDFIX'], bars['MACDSIGNALFIX'], bars['MACDHISTFIX'] = MACDFIX(close, signalperiod=9)
    # bars['MFI'] = MFI(high, low, close, volume, timeperiod=14)
    # bars['MINUS_DI'] = MINUS_DI(high, low, close, timeperiod=14)
    # bars['MINUS_DM'] = MINUS_DM(high, low, timeperiod=14)
    # bars['MOM'] = MOM(close, timeperiod=10)
    # bars['PLUS_DI'] = PLUS_DI(high, low, close, timeperiod=14)
    # bars['PLUS_DM'] = PLUS_DM(high, low, timeperiod=14)
    # bars['PPO'] = PPO(close, fastperiod=12, slowperiod=26, matype=0)
    # bars['ROC'] = ROC(close, timeperiod=10)
    # bars['ROCP'] = ROCP(close, timeperiod=10)
    # bars['ROCR'] = ROCR(close, timeperiod=10)
    # bars['ROCR100'] = ROCR100(close, timeperiod=10)
    # bars['RSI'] = RSI(close, timeperiod=14)
    # bars['SLOWK'], bars['SLOWD'] = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0,
    #                                      slowd_period=3,
    #                                      slowd_matype=0)
    # bars['FASTK'], bars['FASTD'] = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
    # bars['FASTKSRI'], bars['FASTDSRI'] = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    # bars['TRIX'] = TRIX(close, timeperiod=30)
    # bars['ULTOSC'] = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    # bars['WILLR'] = WILLR(high, low, close, timeperiod=14)
    #
    # bars = bars[88:]    # TRIX has 88 NaN values first (the most)
    #
    # print(bars)
    #
    # # start = '2022-01-12T10:00:00-05:00'
    # # end = '2022-01-13T10:00:00-05:00'
    # # start_price = bars['close'][-1]
    #
    # y = bars["close"].tolist()
    #
    # svr = svm.SVR()
    # svr.fit(bars, y)
    # # predictionTime = (datetime.now() + timedelta(hours=5)).timestamp()
    # end_time = '2022-01-13T16:00:00-05:00'  # 6 hours later
    # format2 = "%Y-%m-%dT%H:%M:%S-05:00"
    # prediction_time = datetime.strptime(end_time, format2)
    # prediction = svr.predict([[prediction_time.timestamp()]])
    # print(prediction)



if __name__ == '__main__':
    main()
