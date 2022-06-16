from alpaca_trade_api.rest import REST
from stonkbot import send_message
import keys

api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
account = api.get_account()
positions = api.list_positions()
count = 0
for position in positions:
    sym = position.symbol
    qty = position.qty
    if float(qty) > 0:
        count += 1
        order = api.submit_order(symbol=sym, side="sell", qty=qty)

equity = "${:.2f}".format(float(account.equity))
if count == 0:
    message = "There were no positions to be sold today. The total account equity is " + equity + "."
else:
    message = "I have sold all positions held today. The total number of positions sold was " + str(count) + \
             ". The total account equity after selling is " + equity + "."
# send_message(message)
