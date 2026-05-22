# Cameron Cooke
# Copyright © 2026

"""
This program utilizes Geometric Brownian Motion (GBM) to generate possible price
paths for a portfolio. Using Monte Carlo simulation, the program generates
numerous potential price paths by applying GBM calculation a specified number of
iterations. The results are then displayed in a graphical format.
"""

# import needed libraries
import yfinance as yf
import numpy as np
import pandas as pd

TRADING_DAYS = 252
SIMULATIONS = 10000

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
        portfolioDisplay(positions, shares, rf)

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
This function calculates all needed inputs for GBM calculation.
"""
def GBMInputs(positions, rf):
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
    return s, mu, sig, l, dt

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
def GBMCalculation(positions, s, mu, sig, correlated_z, dt):
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
Monte Carlo Simulation performed running GBM calculation for each trading day
for a specified number of simulations. Each simulation uses the previous day's
price as the starting price. The price path generated for each equity is
adjusted to account for share counts and summed to get portfolio value for each 
simulated trading day.
"""
def monteCarloSimulation(positions, shares, rf):
    s, mu, sig, l, dt = GBMInputs(positions, rf)
    portfolio_path = np.zeros((SIMULATIONS, TRADING_DAYS + 1))
    for iteration in range(0, SIMULATIONS):
        z = np.random.normal(size=(len(positions), TRADING_DAYS))
        correlated_z = l @ z
        price_paths = np.zeros((len(positions), TRADING_DAYS + 1))
        price_paths[:, 0] = s
        portfolio_path[iteration, 0] = np.sum(s * shares)
        for step in range(1, TRADING_DAYS + 1):
            price_paths[:, step] = GBMCalculation(positions, 
                                                    price_paths[:, step - 1], 
                                                    mu, 
                                                    sig, 
                                                    correlated_z[:, step - 1], 
                                                    dt)
            portfolio_path[iteration, step] = np.sum(price_paths[:, step] * shares)
        
    return portfolio_path

"""
Displays metrics in terminal.
"""
def portfolioDisplay(positions, shares, rf):
    portfolio_paths = monteCarloSimulation(positions, shares, rf)
    portfolio_value_before_simulation = portfolio_paths[0, 0]
    average_portfolio_value_after_simulation = np.mean(portfolio_paths[:, -1])

    percent_change = ((average_portfolio_value_after_simulation 
                      / portfolio_value_before_simulation) - 1) * 100

    print("Portfolio before: %.2f" % (portfolio_value_before_simulation))
    print("Average Portfolio after: %.2f" % (average_portfolio_value_after_simulation))
    print("Change percent: %.2f%%" % (percent_change))


if __name__=="__main__":
    main()
    