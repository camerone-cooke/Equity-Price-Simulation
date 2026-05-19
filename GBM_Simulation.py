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


def main():
    # retrieve desired ticker and current risk free rate from user input
    ticker = input('What Equity\'s price would you like to simulate? ')
    rf = float(input('What is the current risk free rate? ')) / 100

    singleGBMCalculation(ticker, rf)

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
def singleGBMCalculation(ticker, rf):
    # preparing inputs needed for calculation
    s = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
    dt = 1 / TRADING_DAYS
    mu = float(expectedReturnCalculation(ticker, rf))
    sig = volatilityCalculation(ticker)
    z = np.random.normal(0, 1)

    # calculating possible future price
    price = s * np.exp(((mu - (0.5 * (sig ** 2))) * dt) + (sig * math.sqrt(dt) * z))
    print("One simulated future price: %.2f" % (price))

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


if __name__=="__main__":
    main()
    