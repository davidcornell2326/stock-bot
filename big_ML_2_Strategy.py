import pickle
import time
from alpaca_trade_api import REST, Stream
from alpaca_trade_api.common import URL
from datetime import datetime, timedelta
import keys
import pandas as pd
from sklearn.neural_network import MLPClassifier, MLPRegressor
import numpy as np
from talib import *

classifiers = {}
bars = pd.DataFrame(data={'high': [], 'low': [], 'open': [], 'close': [], 'volume': [], 'trade_count': [], 'vwap': []})
SYMBOLS = ["AMD", "AAPL", "F", "PLTR", "BAC", "SQ", "ZNGA", "NIO", "OPEN", "NVDA", "ITUB", "SOFI", "T", "AAL",
           "VALE",
           "SWN", "INTC", "NOK", "FL", "FB", "PBR", "BBD", "AMC", "ABEV", "CCL", "RPG", "APA"]


def buy(bar):
    api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    # buy max $300 of each (this covers at least 1 share for all types):
    try:
        qty_owned = int(api.get_position(bar.symbol).qty)
    except:
        qty_owned = 0
    goal_num = 300 // bar.close

    good_time = api.get_clock().is_open and api.get_clock().next_close - api.get_clock().timestamp > timedelta(
        minutes=2)

    if qty_owned < 0:
        if good_time:
            api.submit_order(symbol=bar.symbol, side="buy", qty=abs(qty_owned))  # get to 0
            time.sleep(1)
    num_to_buy = goal_num - max(0, qty_owned)
    api.submit_order(symbol=bar.symbol, side="buy", qty=num_to_buy)  # get to goal_num


def sell(bar):
    # global PROFITS
    api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    try:
        qty_owned = int(api.get_position(bar.symbol).qty)
    except:
        qty_owned = 0
    goal_num = 300 // bar.close

    good_time = api.get_clock().is_open and api.get_clock().next_close - api.get_clock().timestamp > timedelta(
        minutes=2)

    if qty_owned > 0:
        if good_time:
            api.submit_order(symbol=bar.symbol, side="sell", qty=qty_owned)  # get to 0
            time.sleep(1)
    num_to_sell = goal_num - max(0, abs(qty_owned))
    api.submit_order(symbol=bar.symbol, side="sell", qty=num_to_sell)  # get to -(goal_num)


async def bar_callback(b):

    #print(b)
    global bars
    bar = pd.DataFrame(data={'high': [b.high], 'low': [b.low], 'open': [b.open], 'close': [b.close], 'volume': [b.volume], 'trade_count': [b.trade_count], 'vwap': [b.vwap]})
    bars = pd.concat([bars, bar])

    if len(bars) < 89:
        return
    #print("flag 1")
    high = bars['high']
    # continue
    low = bars['low']
    open = bars['open']
    close = bars['close']
    volume = bars['volume']
    #print("flag 2")
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

    # bars = bars[88:]  # TRIX has 88 NaN values first (the most)
    #print("flag 3")
    bars = bars[-89:]     # memory management

    #print(bars.iloc[-1])

    clf = classifiers[b.symbol]
    result = clf.predict([np.array(bars.iloc[-1])])
    print(str(b.symbol) + " at " + str(b.close))
    print(result)


def main():
    global SYMBOLS, classifiers

    stream = Stream(keys.PAPER_API_KEY,
                    keys.PAPER_SECRET_KEY,
                    base_url=URL(keys.PAPER_BASE_URL),
                    data_feed='iex')  # <- replace to SIP if you have PRO subscription

    for symbol in ['AAPL']:
        try:
            classifiers[symbol] = pickle.load(open("./classifiers/clf_" + symbol + ".sav", "rb"))
            print("Loaded classifier for " + symbol)
            stream.subscribe_bars(bar_callback, symbol)
        except:
            print("skipping " + symbol)
            # print(classifiers[symbol])
            continue
    stream.run()

    # results = []
    # for index, rows in test_bars.iterrows():
    #     if index < len(test_bars) - 1:
    #         result = clf.predict([np.array(rows)])
    #         results.append(result[0])
    # actual = []
    # for i in range(len(test_bars) - 1):
    #     _actual = test_bars['close'][i + 1] > test_bars['close'][i]
    #     actual.append(_actual)
    # correct = 0
    # incorrect = 0
    # for i in range(len(results)):
    #     output = results[i] == actual[i]
    #     if output:
    #         correct += 1
    #     else:
    #         incorrect += 1
    #     # print(output)
    # print("Results for " + sym)
    # print("correct: " + str(correct))
    # print("incorrect: " + str(incorrect))
    # print(str(correct / (correct + incorrect)) + "%")
    # print("----------------------------------")


if __name__ == '__main__':
    main()
