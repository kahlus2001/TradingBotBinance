import matplotlib.pyplot as plt


def plot_price_chart(coin, ema_length, symbol, ma_size):
    plt.style.use('dark_background')
    plt.plot(coin['Close'], label='Close Price', color='lightgray', alpha=0.5)
    plt.plot(coin[f'EMA_{ema_length}'], label='EMA_20', color='purple')
    plt.plot(coin[f'SMA_{ma_size}'], label='SMA_30', color='orange')
    #plt.plot(coin['macd'], label='MACD', color='blue')
    #plt.plot(coin['signal_line'], label='Signal Line', color='yellow')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(symbol + ' Price Chart')
    plt.scatter(coin.index, coin['Buy Signals'], label='Buy Signal', marker='^', color='#00ff00')
    plt.scatter(coin.index, coin['Sell Signals'], label='Sell Signal', marker='v', color='#ff0000')
    plt.legend(loc="upper left")
    plt.draw()
    # coin['macd'].plot(label='MACD', color='g')
    # ax = coin['signal_line'].plot(label='Signal Line', color='r')
    # coin['Close'].plot(ax=ax, secondary_y=True, label='Close Price')
    # plt.scatter(coin.index, coin['Buy Signals'], label='Buy Signal', marker='^', color='#00ff00')
    # plt.scatter(coin.index, coin['Sell Signals'], label='Sell Signal', marker='v', color='#ff0000')

    #ax.set_ylabel('MACD')
    # ax.right_ax.set_ylabel('Price $')
    # ax.set_xlabel('Date')
    #lines = ax.get_lines() + ax.right_ax.get_lines()
    # ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
    plt.draw()

