from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
from sklearn import svm
from stonkbot import send_message
import keys


async def trade_callback(t):
    print('trade', t)


async def bar_callback(b):
    print('bar', b)


async def quote_callback(q):
    print('quote', q)


api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
clock = api.get_clock()
timestamp = clock.timestamp
# print(timestamp)
format1 = "%Y-%m-%d %H:%M:%S.%f"
dt = datetime.strptime(str(timestamp)[:-9], format1)
# print(dt)
delta1 = timedelta(minutes=15)
delta2 = timedelta(days=1) + delta1

format2 = "%Y-%m-%dT%H:%M:%S-05:00"  # dependent on UTC-5
start = ((dt - delta2).strftime(format2))
end = ((dt - delta1).strftime(format2))
# print(start)
# print(end)

bars = api.get_bars("AAPL", TimeFrame.Minute, start, end, adjustment='raw').df
# print(bars)
# print("-----------------------------")

timestamps = bars.index.tolist()

X = []
for t in timestamps:
    X.append([int(t.timestamp())])

y = bars["close"].tolist()

svr = svm.SVR()
svr.fit(X, y)
predictionTime = (datetime.now() + timedelta(hours=5)).timestamp()
prediction = svr.predict([[predictionTime]])
'''
print(datetime.fromtimestamp(X[0][0]), y[0])
print(datetime.fromtimestamp(X[1][0]), y[1])
print(datetime.fromtimestamp(X[2][0]), y[2])
print("...")
print(datetime.fromtimestamp(X[-3][0]), y[-3])
print(datetime.fromtimestamp(X[-2][0]), y[-2])
print(datetime.fromtimestamp(X[-1][0]), y[-1])
print(datetime.fromtimestamp(predictionTime), prediction[0])
'''

predicted_price = "${:.2f}".format(prediction[0])
predicted_timestamp = str(datetime.fromtimestamp(predictionTime))[:-7]
most_recent_price = "${:.2f}".format(y[-1])
most_recent_timestamp = str(datetime.fromtimestamp(X[-1][0]))
if prediction[0] > y[-1]:
    # buy $100 worth
    notional = 100
    order = api.submit_order(symbol="AAPL", side="buy", notional=notional)
    buy_price = "${:.2f}".format(notional / float(order.qty))

    message = "BOUGHT. After analyzing the AAPL prices and predicting a price of " + predicted_price + " at " + \
              predicted_timestamp + ", I decided to buy $" + str(notional) + " dollars of AAPL stock. The most recent price was " + \
              most_recent_price + " as of " + most_recent_timestamp + ". The bought price was " + buy_price + "."
else:
    message = "DIDN'T BUY. After analyzing the AAPL prices and predicting a price of " + predicted_price + " at " + \
              predicted_timestamp + ", I decided not to buy any stock. The most recent price was " + most_recent_price + \
              " as of " + most_recent_timestamp + "."
send_message(message)
