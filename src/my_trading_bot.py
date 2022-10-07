from binance.client import Client
import pandas as pd
from plot_chart import *
from collections import Counter
import math

# Author: Mikolaj Kahl: This is a cryptocurrency trading bot, which logs into my Binance account and pulls data using their API.
# It analyzes the data, and based on some technical price indicators, it can place buy or sell orders on the exchange,
# using my account. The trading strategy is still not ideal, and regularly developed. In order to run the code, one
# must have a .txt file with the private and public keys to my binance account.

# get API keys
with open(r'file_with_keys_to_exchange', 'r') as f:
    lines = f.readlines()
    for line in lines:
        words = line.split(',')
public_key, private_key = words[0], words[1]

# log in
client = Client(public_key, private_key)

def get_user_portfolio():
    client_info = client.get_account()
    print(client_info)
    balance = pd.DataFrame(client_info['balances'])
    balance = balance.set_index('asset')
    balance = balance[balance['free'] != '0.00000000']
    print(balance)

get_user_portfolio()

# Specify data
symbol = 'BTCUSDT'
interval = Client.KLINE_INTERVAL_1DAY
period = '365 day'
ema_length = 12
ma_size = 30

# prepare data
window = 7
def get_coin_data(symbol: str, interval, period: str):
    global window
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, period+' ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame[f'EMA_{ema_length}'] =frame['Close'].ewm(span=ema_length).mean()
    frame = frame.astype(float)
    frame['diff'] = frame['Close'].diff(1)
    frame[f'SMA_{ma_size}'] = frame['Close'].rolling(window=ma_size).mean()
    exp1 = frame['Close'].ewm(span=12, adjust=False).mean()
    exp2 = frame['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    print(macd)
    frame['macd'] = macd
    exp3 = macd.ewm(span=9, adjust=False).mean()
    frame['signal_line'] = exp3

    for i in frame.index:
        if i > window:
            frame.at[i, f'{window}_day_diff'] = frame['Close'][i] - frame['Close'][i-window]
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    return frame

coin = get_coin_data(symbol, interval, period)
print(coin[['Close', f'{window}_day_diff', f'SMA_{ma_size}', 'macd', 'signal_line']].tail(10))


# Getting buy and sell signals
buy_signals = []
sell_signals = []
BOUGHT = False

# Strategy

for x in range(len(coin)):

    if coin[f'{window}_day_diff'].iloc[x] > 0 and (coin[f'EMA_{ema_length}'].iloc[x] < coin['Close'].iloc[x]) and (BOUGHT == False):
        buy_signals.append(float(coin["Close"].iloc[x]))
        sell_signals.append(math.nan)

        #order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
        #print(order)
        BOUGHT = True

    elif (coin[f'{window}_day_diff'].iloc[x] <= 0 or (coin[f'EMA_{ema_length}'].iloc[x] > coin['Close'].iloc[x])) and (BOUGHT == True):
        buy_signals.append(math.nan)
        sell_signals.append(float(coin["Close"].iloc[x]))
        # order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
        # print(order)
        BOUGHT = False
    else:
        buy_signals.append(math.nan)
        sell_signals.append(math.nan)
        # print('No trade has been executed')

coin['Buy Signals'] = buy_signals
coin["Sell Signals"] = sell_signals
print(coin)

# plotting (code in other script: plot_chart.py)
plot_price_chart(coin, ema_length, symbol, ma_size)


# compute profit or loss
coin = coin[(coin['Sell Signals'] > 0) | (coin['Buy Signals'] > 0)]
print(coin)
buy_signals = []
sell_signals = []

for row in range(len(coin)):
    buy_signals.append(coin['Buy Signals'].iloc[row])
    sell_signals.append(coin['Sell Signals'].iloc[row])

buys = [p for p in buy_signals if str(p) != 'nan']
sells = [p for p in sell_signals if str(p) != 'nan']

# calculate return from one trade
def one_transaction(invest: float, enter_price: float, exit_price: float):
    amount = invest / enter_price
    investment_return = amount * exit_price - invest
    print(f'You have invested: {invest:.2f}$, and earned: {investment_return:.2f}$ on this particular trade.')
    if investment_return > 0:
        success = True
    else:
        success = False
    return investment_return, success

# calculate total investment return. Input initial starting capital in dollars
def total_return(start: int) -> None:
    siano = start
    successes = []
    for i in range(len(buys)-1):
        call = one_transaction(siano, buys[i], sells[i])
        siano = siano + call[0]
        successes.append(call[1])
    profit = siano-start
    print(f'You have started with {start:.2f}$, and ended up with {siano:.2f}$. This is {profit:.2f}$ profit.')
    success_counter = Counter(successes)
    success_rate = 100 * success_counter[True] / (success_counter[True] + success_counter[False])
    print(f'{success_rate:.2f}% of trades were successful trades.')
    percent_profit = siano / start * 100 - 100
    print(f'Your portfolio grew in value by {percent_profit:.2f}%.')
    return None

print(total_return(10))
plt.show()



