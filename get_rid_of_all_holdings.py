from alpaca_trade_api.rest import REST
import keys

if __name__ == '__main__':
    api = REST(key_id=keys.PAPER_API_KEY, secret_key=keys.PAPER_SECRET_KEY, base_url=keys.PAPER_BASE_URL)
    for position in api.list_positions():
        sym = position.symbol
        qty = int(position.qty)
        if qty > 0:
            api.submit_order(symbol=sym, side="sell", qty=qty)
        elif qty < 0:
            api.submit_order(symbol=sym, side="buy", qty=abs(qty))
