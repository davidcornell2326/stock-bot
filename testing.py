import time

import keys
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
from sklearn import svm

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
#
#
# async def bar_callback(b):
#     global val
#     if b.c > val:
#         print("Up")
#     elif b.c < val:
#         print("Down")
#     else:
#         print("Equal")
#     val = b.c
#
#
# # Initiate Class Instance
# stream = Stream(keys.PAPER_API_KEY,
#                 keys.PAPER_SECRET_KEY,
#                 base_url=URL(keys.PAPER_BASE_URL),
#                 data_feed='iex')  # <- replace to SIP if you have PRO subscription
#
# stream.subscribe_bars(bar_callback, 'AAPL')
# stream.run()

def main():
    print("flag")
    api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    clock = api.get_clock()
    timestamp = clock.timestamp
    # print(timestamp)
    format1 = "%Y-%m-%d %H:%M:%S.%f"
    dt = datetime.strptime(str(timestamp)[:-9], format1)
    # print(dt)
    delta1 = timedelta(minutes=15)
    delta2 = timedelta(days=4) + delta1

    format2 = "%Y-%m-%dT%H:%M:%S-05:00"  # dependent on UTC-5
    start = ((dt - delta2).strftime(format2))
    end = ((dt - delta1).strftime(format2))
    # print(start)
    # print(end)

    bars = api.get_bars("AAPL", TimeFrame.Minute, start, end, adjustment='raw').df
    print(bars)




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