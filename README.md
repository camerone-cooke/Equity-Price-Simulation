# GBM Portfolio Simulator

Monte Carlo portfolio simulator using Geometric Brownian Motion with correlated asset shocks and live market data.

---

## Project Synopsis

This program simulates potential future values of an equity portfolio using Geometric Brownian Motion and Monte Carlo simulation. Live market data is pulled from Yahoo Finance via the yfinance library and used to compute expected returns, historical volatility, and correlations between asset pairs. The simulation generates 10,000 price paths for the portfolio and outputs a graphical display of the data along with relevant metrics including VaR, Sharpe ratio, Sortino ratio, and probability of loss.

---

## Technical Approach

### Monte Carlo Simulation

#### What is a Monte Carlo simulation?

A Monte Carlo simulation is a way to model the probability of different outcomes for a process whose outcome cannot be easily predicted due to the inclusion of a random variable(s). The Monte Carlo technique is used to understand the impact of risk and uncertainty and in investing is used to model the range of future prices of an asset. 

#### Monte Carlo simulation used in this project

In the context of this project, Monte Carlo simulation is being used to estimate thousands of possible future values of an equity portfolio. The underlying process modeled in this program is Geometric Brownian Motion. Utilizing a Monte Carlo simulation allows investors to better grasp the range of possible outcomes and their relative likelihood. This also allows for the estimation of the probability of loss, and quantifying downside risk via metrics like Value at Risk.
