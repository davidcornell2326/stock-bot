from alpaca_trade_api import REST, TimeFrame
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
import keys
from datetime import datetime, timedelta

async def trade_callback(t):
    print('trade', t)


async def quote_callback(q):
    print('quote', q)

async def bar_callback(b):
    print('bar', b)



# # Initiate Class Instance
# stream = Stream(keys.REAL_API_KEY,
#                 keys.REAL_SECRET_KEY,
#                 base_url=URL('https://api.alpaca.markets'),
#                 data_feed='iex')  # <- replace to SIP if you have PRO subscription
#
# # subscribing to event
# # stream.subscribe_trades(trade_callback, 'AAPL')
# stream.subscribe_bars(bar_callback, 'AAPL')
# # stream.subscribe_quotes(quote_callback, 'IBM')
#
# print("run")
#
# stream.run()




if __name__ == '__main__':
    # api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    # close = api.get_clock().next_close
    # current = api.get_clock().timestamp
    # print(close - current > timedelta(minutes=1))
    # print(current)

    # bars = api.get_bars("AAPL", TimeFrame.Minute, "2022-03-31T09:30:00-04:00", "2022-03-31T10:30:00-04:00")
    # print(len(bars))

    stream = Stream(keys.REAL_API_KEY,
                    keys.REAL_SECRET_KEY,
                    base_url=URL('https://api.alpaca.markets'),
                    data_feed='iex')  # <- replace to SIP if you have PRO subscription

    # subscribing to event
    # stream.subscribe_trades(trade_callback, 'AAPL')
    stream.subscribe_bars(bar_callback, 'AAPL')
    # stream.subscribe_quotes(quote_callback, 'IBM')

    print("run")

    stream.run()