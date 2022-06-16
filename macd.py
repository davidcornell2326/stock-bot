import time
from datetime import datetime, timedelta
from alpaca_trade_api import Stream, REST, TimeFrame
from alpaca_trade_api.common import URL
import keys
from statistics import mean
from stonkbot import send_message
import signal

SYMBOLS = ["AMD", "AAPL", "F", "PLTR", "BAC", "SQ", "ZNGA", "NIO", "OPEN", "NVDA", "ITUB", "SOFI", "T", "AAL", "VALE",
           "SWN", "INTC", "NOK", "FL", "FB", "PBR", "BBD", "AMC", "ABEV", "CCL", "RPG", "APA"]
BOUGHT_PRICES = {}
PROFITS = {}


def handler(signum, frame):
    # global PROFITS
    # print(PROFITS)
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


def buy(bar):
    # global BOUGHT_PRICES
    # BOUGHT_PRICES[bar.symbol] = bar.close  # approximate, may change by the time order is fulfilled
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
    if good_time:
        num_to_sell = goal_num - max(0, abs(qty_owned))
        api.submit_order(symbol=bar.symbol, side="sell", qty=num_to_sell)  # get to -(goal_num)

    # if bar.symbol not in PROFITS:
    #     PROFITS[bar.symbol] = 0
    # PROFITS[bar.symbol] += (bar.close - BOUGHT_PRICES[bar.symbol]) * num_to_negative_1  # approximate, may change by time order is fulfilled


prices = {}
ema_12 = {}
ema_26 = {}
macd = {}
signal_line = {}
differences = {}


async def bar_callback(b):  # async
    global prices
    global ema_12
    global ema_26
    global macd
    global signal_line
    global differences

    if b.symbol not in prices:
        prices[b.symbol] = []
    if b.symbol not in ema_12:
        ema_12[b.symbol] = []
    if b.symbol not in ema_26:
        ema_26[b.symbol] = []
    if b.symbol not in macd:
        macd[b.symbol] = []
    if b.symbol not in signal_line:
        signal_line[b.symbol] = []
    if b.symbol not in differences:
        differences[b.symbol] = []

    # memory control
    # only use negative indices to reference past data points; assume length is not known
    if len(prices[b.symbol]) > 100:
        prices[b.symbol].pop(0)
    if len(ema_12[b.symbol]) > 100:
        ema_12[b.symbol].pop(0)
    if len(ema_26[b.symbol]) > 100:
        ema_26[b.symbol].pop(0)
    if len(macd[b.symbol]) > 100:
        macd[b.symbol].pop(0)
    if len(signal_line[b.symbol]) > 100:
        signal_line[b.symbol].pop(0)
    if len(differences[b.symbol]) > 100:
        differences[b.symbol].pop(0)

    # print(b)
    prices[b.symbol].append(b.close)  # ************ b.S or b.symbol??

    if len(prices[b.symbol]) == 12:
        ema_12[b.symbol].append(mean(prices[b.symbol]))
    if len(prices[b.symbol]) > 12:
        k = 2.0 / (12 + 1)
        ema_12[b.symbol].append(prices[b.symbol][-1] * k + ema_12[b.symbol][-1] * (1 - k))
    if len(prices[b.symbol]) == 26:
        ema_26[b.symbol].append(mean(prices[b.symbol]))
    if len(prices[b.symbol]) > 26:
        k = 2.0 / (26 + 1)
        ema_26[b.symbol].append(prices[b.symbol][-1] * k + ema_26[b.symbol][-1] * (1 - k))

    if len(prices[b.symbol]) > 26:
        macd[b.symbol].append(ema_12[b.symbol][-1] - ema_26[b.symbol][-1])

    if len(macd[b.symbol]) == 9:
        signal_line[b.symbol].append(mean(macd[b.symbol]))
    if len(macd[b.symbol]) > 9:
        k = 2.0 / (9 + 1)
        signal_line[b.symbol].append(macd[b.symbol][-1] * k + signal_line[b.symbol][-1] * (1 - k))

    if len(signal_line[b.symbol]) > 0:
        differences[b.symbol].append(macd[b.symbol][-1] - signal_line[b.symbol][-1])

    # now, macd and signal are the two lines, and differences is the difference between them

    x = ""

    if len(differences[b.symbol]) > 1:
        if differences[b.symbol][-1] > 0 and differences[b.symbol][-1] > differences[b.symbol][-2]:
            x += "dark green"
            sell(b)
        if differences[b.symbol][-1] > 0 and differences[b.symbol][-1] <= differences[b.symbol][-2]:
            x += "ligh green"
        if differences[b.symbol][-1] <= 0 and differences[b.symbol][-1] <= differences[b.symbol][-2]:
            x += "dark red"
            buy(b)
        if differences[b.symbol][-1] <= 0 and differences[b.symbol][-1] > differences[b.symbol][-2]:
            x += "ligh red"
            buy(b)
    else:
        x += "length of prices: " + str(len(prices[b.symbol]))

    print(x)
    # print(PROFITS)
    # print(BOUGHT_PRICES)


def main():
    global SYMBOLS

    print("starting")

    signal.signal(signal.SIGINT, handler)

    stream = Stream(keys.PAPER_API_KEY,
                    keys.PAPER_SECRET_KEY,
                    base_url=URL(keys.PAPER_BASE_URL),
                    data_feed='iex')  # <- replace to SIP if you have PRO subscription

    for symbol in SYMBOLS:
        stream.subscribe_bars(bar_callback, symbol)
    stream.run()

    # api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    # clock = api.get_clock()
    # timestamp = clock.timestamp
    # # print(timestamp)
    # format1 = "%Y-%m-%d %H:%M:%S.%f"
    # dt = datetime.strptime(str(timestamp)[:-9], format1)
    # # print(dt)
    # delta1 = timedelta(days=4)
    # delta2 = timedelta(days=1) + delta1
    #
    # format2 = "%Y-%m-%dT%H:%M:%S-05:00"  # dependent on UTC-5
    # start = ((dt - delta2).strftime(format2))
    # end = ((dt - delta1).strftime(format2))
    # # print(start)
    # # print(end)
    #
    # bars = api.get_bars("AAPL", TimeFrame.Minute, start, end, adjustment='raw').df
    # print(bars)
    # for bar in bars["close"]:
    #     # print(bar)
    #     bar_callback(bar)


if __name__ == '__main__':
    main()
