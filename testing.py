import time

import pandas as pd
import numpy as np

import simulator
import keys
import pprint
import pickle
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
from sklearn import svm
import pandas
from talib._ta_lib import *
from os.path import exists

def main():
    for i in range(10):
        # pd.set_option('display.max_columns', None)
        # clf = pickle.load(open("./classifiers/clf_AAPL.sav", "rb"))
        bars = pd.read_csv('./bars/bars_AAPL_2021.csv')
        decisions = np.random.choice([True, False], size=len(bars))
        # decisions = [False for _ in range(len(bars))]
        simulator.simulate_trades(bars, decisions)


# print("start")
# api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
# api.submit_order(symbol="AAPL", side="sell", qty=1)
# print("done")


# def sendEmail(message):
#     import smtplib, ssl
#
#     port = 465  # For SSL
#     password = "xfrhfaqsuvglclmu"
#     sender_email = "thoughtswithjeffyt@gmail.com"
#     receiver_email = "davidcornell2326@gmail.com"
#
#     # Create a secure SSL context
#     context = ssl.create_default_context()
#
#     with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#         server.login("thoughtswithjeffyt@gmail.com", password)
#         server.sendmail(sender_email, receiver_email, message)

# val = 0


# async def bar_callback(b):
#     print("-")
#     global val
#     if b.c > val:
#         print("Up")
#     elif b.c < val:
#         print("Down")
#     else:
#         print("Equal")
#     val = b.c


# def main():
#     print("starting")
# Initiate Class Instance
# stream = Stream(keys.PAPER_API_KEY,
#                 keys.PAPER_SECRET_KEY,
#                 base_url=URL(keys.PAPER_BASE_URL),
#                 data_feed='iex')  # <- replace to SIP if you have PRO subscription
#
# stream.subscribe_bars(bar_callback, 'AAPL')
# stream.run()


# print("flag")
# def main():
#     pass
    # SYMBOLS = ["AMD", "AAPL", "F", "PLTR", "BAC", "SQ", "ZNGA", "NIO", "OPEN", "NVDA", "ITUB", "SOFI", "T", "AAL",
    #            "VALE",
    #            "SWN", "INTC", "NOK", "FL", "FB", "PBR", "BBD", "AMC", "ABEV", "CCL", "RPG", "APA"]
    #
    # api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    #
    # for sym in SYMBOLS:
    #     for year in ['2018', '2019', '2020', '2021']:
    #         if exists('./modified_bars/bars_' + sym + '_' + year + '.csv'):
    #             print("skipping")
    #             continue
    #         bars = pandas.read_csv('./bars/bars_' + sym + '_' + year + '.csv')
    #
    #         try:
    #             high = bars['high']
    #             low = bars['low']
    #             open = bars['open']
    #             close = bars['close']
    #             volume = bars['volume']
    #         except:
    #             break
    #
    #         # ALL Momentum Indicators:
    #         bars['ADX'] = ADX(high, low, close, timeperiod=14)
    #         bars['ADXR'] = ADXR(high, low, close, timeperiod=14)
    #         bars['APO'] = APO(close, fastperiod=12, slowperiod=26, matype=0)
    #         bars['AROONDOWN'], bars['AROONUP'] = AROON(high, low, timeperiod=14)
    #         bars['AROONSC'] = AROONOSC(high, low, timeperiod=14)
    #         bars['BOP'] = BOP(open, high, low, close)
    #         bars['CCI'] = CCI(high, low, close, timeperiod=14)
    #         bars['CMO'] = CMO(close, timeperiod=14)
    #         bars['DX'] = DX(high, low, close, timeperiod=14)
    #         bars['MACD'], bars['MACDSIGNAL'], bars['MACDHIST'] = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    #         bars['MACDEXT'], bars['MACDSIGNALEXT'], bars['MACDHISTEXT'] = MACDEXT(close, fastperiod=12, fastmatype=0,
    #                                                                               slowperiod=26, slowmatype=0,
    #                                                                               signalperiod=9, signalmatype=0)
    #         bars['MACDFIX'], bars['MACDSIGNALFIX'], bars['MACDHISTFIX'] = MACDFIX(close, signalperiod=9)
    #         bars['MFI'] = MFI(high, low, close, volume, timeperiod=14)
    #         bars['MINUS_DI'] = MINUS_DI(high, low, close, timeperiod=14)
    #         bars['MINUS_DM'] = MINUS_DM(high, low, timeperiod=14)
    #         bars['MOM'] = MOM(close, timeperiod=10)
    #         bars['PLUS_DI'] = PLUS_DI(high, low, close, timeperiod=14)
    #         bars['PLUS_DM'] = PLUS_DM(high, low, timeperiod=14)
    #         bars['PPO'] = PPO(close, fastperiod=12, slowperiod=26, matype=0)
    #         bars['ROC'] = ROC(close, timeperiod=10)
    #         bars['ROCP'] = ROCP(close, timeperiod=10)
    #         bars['ROCR'] = ROCR(close, timeperiod=10)
    #         bars['ROCR100'] = ROCR100(close, timeperiod=10)
    #         bars['RSI'] = RSI(close, timeperiod=14)
    #         bars['SLOWK'], bars['SLOWD'] = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0,
    #                                              slowd_period=3,
    #                                              slowd_matype=0)
    #         bars['FASTK'], bars['FASTD'] = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
    #         bars['FASTKSRI'], bars['FASTDSRI'] = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3,
    #                                                       fastd_matype=0)
    #         bars['TRIX'] = TRIX(close, timeperiod=30)
    #         bars['ULTOSC'] = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    #         bars['WILLR'] = WILLR(high, low, close, timeperiod=14)
    #
    #         bars = bars[88:]  # TRIX has 88 NaN values first (the most)
    #
    #         bars.to_csv('./modified_bars/bars_' + sym + '_' + year + '.csv', index=False)
    #         print("wrote " + './modified_bars/bars_' + sym + '_' + year + '.csv')



# # MACD


# # importing the required module
# import matplotlib.pyplot as plt
#
# # x axis values
# x = []
# for val in X:
#     x.append(datetime.fromtimestamp(val[0]))
# # x.append(datetime.fromtimestamp(now))
# # corresponding y axis values
# y = y
# # y.append(prediction[0])
#
# # print(x[-3], y[-3])
# # print(x[-2], y[-2])
# # print(x[-1], y[-1])
#
# # plotting the points
# plt.plot(x, y)
#
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
#
# # giving a title to my graph
# plt.title('My first graph!')
#
# # function to show the plot
# plt.show()

if __name__ == '__main__':
    main()
