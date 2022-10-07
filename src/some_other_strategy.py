# BE CAREFUL, CALLING THIS FUNCTION WILL SET A REAL ORDER ON BINANCE!!!
def strategy(symbol, quantity, entried=False):
    df = get_coin_data(symbol,'1m', '30m')
    cumulative_return = (df.Open.pct_change() + 1).cumprod() - 1
    if not entried:
        if cumulative_return[-1] < -0.002:  # buying condition
            order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
            print(order)
            entried = True
        else:
            print('No trade has been executed')
    if entried:
        while True:
            df = get_coin_data(symbol,'1m', '30m')
            since_buy = df.loc[df.index > pd.to_datetime(order['transactTime'], unit='ms')]
            if len(since_buy) > 0:
                return_since_buy = (since_buy.Open.pct_change() + 1).cumprod() - 1
                if return_since_buy[-1] > 0.0015 or return_since_buy[-1] < -0.0015:   # selling condition
                    order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
                    print(order)
                    break

 #moja strategia
    if coin['7_day_diff'].iloc[x] > 0 and (coin[f'EMA_{ema_length}'].iloc[x] < coin['Close'].iloc[x]) and (BOUGHT == False):
        buy_signals.append(float(coin["Close"].iloc[x]))
        sell_signals.append(math.nan)
        # order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
        # print(order)
        BOUGHT = True
    elif (coin['7_day_diff'].iloc[x] <= 0 or coin['7_day_diff'].iloc[x] < -0.002 * coin['Close'].iloc[x]) and (BOUGHT == True):
        buy_signals.append(math.nan)
        sell_signals.append(float(coin["Close"].iloc[x]))
        # order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
        # print(order)
        BOUGHT = False
    else:
        buy_signals.append(math.nan)
        sell_signals.append(math.nan)
        #print('No trade has been executed')

        if coin[f'EMA_{ema_length}'].iloc[x] < coin['Close'].iloc[x] and (BOUGHT == False):
            buy_signals.append(float(coin["Close"].iloc[x]))
            sell_signals.append(math.nan)
            # order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
            # print(order)
            BOUGHT = True
        elif coin[f'EMA_{ema_length}'].iloc[x] > coin['Close'].iloc[x] and (BOUGHT == True):
            buy_signals.append(math.nan)
            sell_signals.append(float(coin["Close"].iloc[x]))
            # order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
            # print(order)
            BOUGHT = False
        else:
            buy_signals.append(math.nan)
            sell_signals.append(math.nan)
            # print('No trade has been executed')