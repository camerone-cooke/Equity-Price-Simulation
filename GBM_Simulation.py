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
import pandas as pd

TRADING_DAYS = 252

"""
Check if number of positions is valid and then run simulation on portfolio.
"""
def main():
    positions, shares = getPortfolio()
    if (len(positions) < 1):
        print("No positions given")
    else:
        # prompt user for risk free rate
        rf = float(input('What is the current risk free rate? ')) / 100
        portfolioCalculation(positions, shares, rf)

"""
Prompt user for positions in portfolio and number of shares of each position.
"""
def getPortfolio():
    positions = np.array([])
    shares = np.array([])
    # prompt user for ticker
    ticker = input('What Equity\'s price would you like to simulate? '
                    'or \'quit\' to stop: ')
    while (ticker != "quit"):
        # prompt user for number of shares of equity
        share_count = int(input('How many Shares of this equity? '))

        # add ticker to positions and number of shares to shares
        positions = np.append(positions, ticker)
        shares = np.append(shares, share_count)
        
        # re-prompt user for next ticker
        ticker = input('What Equity\'s price would you like to simulate? '
                    'or \'quit\' to stop: ')
        
    return positions, shares

"""
Geometric Brownian Motion (GBM) is calculated using the formula:
price = s * np.exp(((mu - (0.5 * (sig ** 2))) * dt) + (sig * np.sqrt(dt) * z))
Where: 
s = current price of equity
mu = expected return
sig = volatility
dt = time delta
correlated_z = correlated random shock
"""
def GBMCalculation(positions, rf):
    # preparing inputs needed for calculation
    dt = 1 / TRADING_DAYS

    s = np.array([])
    mu = np.array([])
    sig = np.array([])

    for index in range(len(positions)):
        s = np.append(s, 
                        yf.Ticker(positions[index]).history(period="1d")["Close"].iloc[-1])
        mu = np.append(mu, float(expectedReturnCalculation(positions[index], rf)))
        sig = np.append(sig, volatilityCalculation(positions[index]))
    
    corr_matrix = correlationCalculation(positions)
    cov_matrix = np.outer(sig, sig) * corr_matrix
    l = np.linalg.cholesky(cov_matrix)

    z = np.random.normal(size=len(positions))
    correlated_z = l @ z

    # calculate possible future price(s)
    future_prices = np.array([])
    for index in range(0, len(positions)):
        drift = (mu[index] - (0.5 * (sig[index] ** 2))) * dt
        diffusion = (sig[index] * np.sqrt(dt) * correlated_z[index])
        next_price = s[index] * np.exp(drift + diffusion)
        future_prices = np.append(future_prices,  next_price)

    return future_prices

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
sig = daily_volatility * np.sqrt(252)
"""
def volatilityCalculation(ticker):
    historical_price_data = yf.Ticker(ticker).history(period='1y')['Close']
    logarithmic_returns = np.log(historical_price_data 
                                 / historical_price_data.shift(1))
    cleaned_returns = logarithmic_returns.dropna()
    daily_volatility = cleaned_returns.std()
    sig = daily_volatility * np.sqrt(TRADING_DAYS)
    return sig

"""
Correlation measures the degree to which two equities move in lock-step with one
another. Their correlation value can range from -1.0 (inversely correlated) to
1.0 (positively correlated). The correlation matrix is calculated by taking
logarithmic returns of each equity in the portfolio and computing the pairwise
correlation coefficients between all equity pairs.
"""
def correlationCalculation(positions):
    historical_price_data = pd.DataFrame()
    for index in range(0, len(positions)):
        historical_price_data[positions[index]] = yf.Ticker(positions[index]).history(period='1y')['Close']
    logarithmic_returns = np.log(historical_price_data 
                                 / historical_price_data.shift(1))
    cleaned_returns = logarithmic_returns.dropna()
    corr_matrix = np.array(cleaned_returns.corr())
    return corr_matrix

"""
Calculates total value of portfolio before and after simulation of individual
equities. Also calculates the percent change in total portfolio value. Prints 
results to console.
"""
def portfolioCalculation(positions, shares, rf):
    portfolio_value_before_simulation = 0
    for index in range(0, len(positions)):
        price = yf.Ticker(positions[index]).history(period="1d")["Close"].iloc[-1]
        total_equity_allocation_value = price * shares[index]
        portfolio_value_before_simulation += total_equity_allocation_value

    portfolio_value_after_simulation = 0
    simulated_prices = GBMCalculation(positions, rf)
    for index in range(0, len(positions)):
        total_equity_allocation_value = simulated_prices[index] * shares[index]
        portfolio_value_after_simulation += total_equity_allocation_value

    percent_change = ((portfolio_value_after_simulation 
                      / portfolio_value_before_simulation) - 1) * 100

    print("Portfolio before: %.2f" % (portfolio_value_before_simulation))
    print("Portfolio after: %.2f" % (portfolio_value_after_simulation))
    print("Change percent: %.2f%%" % (percent_change))


if __name__=="__main__":
    main()
    