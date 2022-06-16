def simulate_trades(bars, decisions):
    # print(bars.head())
    # print('------------------')
    # print(decisions[:5])
    # print('------------------')
    if len(bars) != len(decisions):
        print('Unequal lengths')
        print(f'Bars: {len(bars)}')
        print(f'Decisions: {len(decisions)}')

    liquid = 100000
    shares_owned = 0

    # always go to 10 or -10 shares
    for i,bar in bars.iterrows():
        if i == 0:
            if decisions[i]:
                # buy 10
                liquid -= 10 * bar.close
                shares_owned += 10
            else:
                # sell 10
                liquid += 10 * bar.close
                shares_owned -= 10
            continue
        # print(i)
        # break
        # 4 combinations, act on 2 of them, hold (pass) on the other 2:
        if decisions[i]:
            if shares_owned < 0:
                # buy 20
                # print('buy')
                liquid -= 20 * bar.close
                shares_owned += 20
            else:
                # print('hold')
                pass
        else:
            if shares_owned > 0:
                # sell 20
                # print('sell')
                liquid += 20 * bar.close
                shares_owned -= 20
            else:
                # print('hold')
                pass
    # liquidate
    if shares_owned < 0:
        # buy 10
        # print('buy')
        liquid -= 10 * bar.close
        shares_owned += 10
    elif shares_owned > 0:
        # sell 10
        # print('sell')
        liquid += 10 * bar.close
        shares_owned -= 10
    print('Simulator Results:')
    print(f'Shares owned: {shares_owned}')
    print(f'Liquid: {liquid}')