import yfinance as yf
import ta
import pandas as pd
import matplotlib.pyplot as plt


# something is wrong in the loop

start_date = '2018-01-01'
asset = 'EURUSD=X'
df = yf.download(asset, start=start_date)

stock_k_threshold = 0.05   # tweak
def indicators(df):
    df['SMA_200'] = ta.trend.sma_indicator(df.Close, window=200)
    df['stoch_k'] = ta.momentum.stochrsi_k(df.Close, window=10)
    df.dropna(inplace=True)
    df['Buy'] = (df.Close > df.SMA_200) & (df.stoch_k < stock_k_threshold)

indicators(df)

buydates, selldates = [], []
buys, sells = [], []
last_selldate = pd.to_datetime('1900-01-01')

for row in range(len(df)):
    if len(selldates) > 0:
        last_selldate = selldates[-1]
    if df.iloc[row].Buy:
        buyprice = df.iloc[row].Close * 0.97   # 3% limit order. to tweak
        k = 1
        buydate = None
        while True:
            if row + k >= len(df):
                break
            if buyprice >= df.iloc[row + k].Low:
                buydate = df.iloc[row + k].name  # timestamp
                break
            elif k > 10:    # threshold. to tweak
                break
            else:
                k += 1
        if row + k + 11 >= len(df):
            break
        if (buydate is not None) and (buydate > last_selldate):
            buydates.append(buydate)
            buys.append(buyprice)
            for j in range(1, 11):    # to tweak
                if row + k + j + 1 >= len(df):
                    break
                if df.iloc[row + k + j].Close > buyprice:
                    sellprice = df.iloc[row + k + j + 1].Open
                    selldate = df.iloc[row + k + j + 1].name
                    sells.append(sellprice)
                    selldates.append(selldate)
                    break
                elif j == 10:
                    sellprice = df.iloc[row + k + j + 1].Open
                    selldate = df.iloc[row + k + j + 1].name
                    sells.append(sellprice)
                    selldates.append(selldate)
                    break

print("Buydates:")
print(buydates)
print("Selldates")
print(selldates)


profits = pd.DataFrame([(sell-buy)/buy for sell, buy in zip(sells, buys)])

cum_profits = (profits + 1).cumprod()
pct_change = (df.Close.pct_change() + 1).cumprod()

print(f'Buying {asset} on {start_date} and holding would yield return of {pct_change.iloc[-1]}.')
print(f'Trading {asset} since {start_date} would yield return of {str(cum_profits.iloc[-1].values)}.')

plt.plot(df.Close)
plt.scatter(df.loc[buydates].index, df.loc[buydates].Close, marker='^', c='g')
plt.scatter(df.loc[selldates].index, df.loc[buydates].Close, marker='v', c='r')
plt.show()