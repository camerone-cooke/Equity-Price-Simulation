# Cameron Cooke
# Copyright © 2026

"""
This program utilizes Geometric Brownian Motion (GBM) to generate possible price
paths for a selected equity. Using Monte Carlo simulation, the program generates
numerous potential price paths by applying GBM calculation a specified number of
iterations. The results are then displayed in a graphical format.
"""

# import needed libraries
import yfinance as yf
import numpy as np
import math

TRADING_DAYS = 252
positions = []
shares = []

"""
Prompt user for positions in portfolio and number of shares of each position.
Check if number of positions is valid and then run simulation on portfolio.
Return the before and after value of portfolio along with percent change.
"""
def main():
    # prompt user for ticker
    ticker = input('What Equity\'s price would you like to simulate? '
                    'or \'quit\' to stop: ')
    while (ticker != "quit"):
        # prompt user for number of shares of equity
        share_count = int(input('How many Shares of this equity? '))

        # add ticker to positions and number of shares to shares
        positions.append(ticker)
        shares.append(share_count)
        
        # re-prompt user for next ticker
        ticker = input('What Equity\'s price would you like to simulate? '
                    'or \'quit\' to stop: ')

    if (len(positions) < 1):
        print("No positions given")
    else:
        # prompt user for risk free rate
        rf = float(input('What is the current risk free rate? ')) / 100
        if (len(positions) == 1):
            portfolioCalculation(positions, shares, rf)
        else:
            portfolioCalculation(positions, shares, rf)

"""
Geometric Brownian Motion (GBM) is calculated using the formula:
price = s * np.exp(((mu - (0.5 * (sig ** 2))) * dt) + (sig * math.sqrt(dt) * z))
Where: 
s = current price of equity
mu = expected return
sig = volatility
dt = time delta
z = random shock
"""
def GBMCalculation(ticker, rf):

    # preparing inputs needed for calculation
    s = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
    dt = 1 / TRADING_DAYS
    mu = float(expectedReturnCalculation(ticker, rf))
    sig = volatilityCalculation(ticker)
    z = np.random.normal(0, 1)

    # calculating possible future price
    price = s * np.exp(((mu - (0.5 * (sig ** 2))) * dt) + (sig * math.sqrt(dt) * z))
    return price

"""
Expected return is utilized in GBM to calculate the drift factor and is 
determined using the Capital Asset Pricing Model (CAPM) whose formula is:
mu = rf + ba * rp
Where:
mu = expected return
rf = risk free rate
ba = beta of equity
rp = equity risk premium
"""
def expectedReturnCalculation(ticker, rf):
    ba = yf.Ticker(ticker).info.get('beta')
    rm = ((yf.Ticker('SPY').history(period="10y")['Close'].iloc[-1] 
           / yf.Ticker('SPY').history(period="10y")['Close'].iloc[0]) 
           ** (1 / 10)) - 1
    rp = (rm - rf)
    mu = rf + (ba * rp)
    return mu

"""
Sigma is the standard deviation of the equity's returns and is utilized in GBM 
as the magnitude of the 'shocks'. Sigma is determined by taking the daily 
logarithmic returns of the equity. The formula for determining sigma is:
sig = daily_volatility * sqrt(252)
"""
def volatilityCalculation(ticker):
    historical_price_data = yf.Ticker(ticker).history(period='1y')['Close']
    logarithmic_returns = np.log(historical_price_data 
                                 / historical_price_data.shift(1))
    cleaned_returns = logarithmic_returns.dropna()
    daily_volatility = cleaned_returns.std()
    sig = daily_volatility * math.sqrt(TRADING_DAYS)
    return sig

def portfolioCalculation(positions, shares, rf):
    portfolio_value_before_simulation = 0
    for index in range(0, len(positions)):
        price = yf.Ticker(positions[index]).history(period="1d")["Close"].iloc[-1]
        total_equity_allocation_value = price * shares[index]
        portfolio_value_before_simulation += total_equity_allocation_value

    portfolio_value_after_simulation = 0
    for index in range(0, len(positions)):
        simulated_price = GBMCalculation(positions[index], rf)
        total_equity_allocation_value = simulated_price * shares[index]
        portfolio_value_after_simulation += total_equity_allocation_value

    percent_change = ((portfolio_value_after_simulation 
                      / portfolio_value_before_simulation) - 1) * 100

    print("Portfolio before: %.2f" % (portfolio_value_before_simulation))
    print("Portfolio after: %.2f" % (portfolio_value_after_simulation))
    print("Change percent: %.2f%%" % (percent_change))



if __name__=="__main__":
    main()
    