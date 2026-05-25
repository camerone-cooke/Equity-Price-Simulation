# GBM Portfolio Simulator

Monte Carlo portfolio simulator using Geometric Brownian Motion with correlated asset shocks and live market data.

---

## Project Synopsis

This program simulates potential future values of an equity portfolio using Geometric Brownian Motion and Monte Carlo simulation. Live market data is pulled from Yahoo Finance via the yfinance library and used to compute expected returns, historical volatility, and correlations between asset pairs. The simulation generates 10,000 price paths for the portfolio and outputs a graphical display of the data along with relevant metrics including VaR, Sharpe ratio, Sortino ratio, and probability of loss.

---

## Technical Approach

### Monte Carlo Simulation

#### What is Monte Carlo simulation?

Monte Carlo simulation is a way to model the probability of different outcomes for a process whose outcome cannot be easily predicted due to the inclusion of a random variable(s). Monte Carlo simulation is used to understand the impact of risk and uncertainty and in investing can be used to model the range of future prices of an asset. 

#### Monte Carlo simulation used in this project

In the context of this project, Monte Carlo simulation is being used to estimate thousands of possible future values of an equity portfolio. The underlying process modeled in this program is Geometric Brownian Motion. Utilizing a Monte Carlo simulation allows investors to better grasp the range of possible outcomes and their relative likelihood. This also allows for the estimation of the probability of loss, and quantifying downside risk via metrics like Value at Risk.

### Geometric Brownian Motion

#### What is Geometric Brownian Motion?

Geometric Brownian Motion (GBM) is a stochastic process used to model the evolution of an asset's price. The process originated from Brownian Motion, a concept from physics that was observed through the random movement of pollen particles in water. The "Geometric" extension came later to modify the process for the modeling of asset prices, ensuring they stay positive and grow multiplicatively. GBM assumes that asset prices follow a log-normal distribution, and therefore logarithmic returns are normally distributed. GBM is the foundation of many financial models including Black-Scholes option pricing.

#### Geometric Brownian Motion as a Concept

Geometric Brownian Motion is best understood through analogy. Consider a leaf floating down a river. Its movement is determined by two forces, the current of the river which pushes the leaf in a general direction (drift), and the deviations caused by branches, rocks, other objects in the water, and wind (random shocks). The prices of equities behave in the same manner. Expected return acts as the drift, providing a constant directional pull, while market randomness introduces volatility at each time step. GBM captures these two forces and utilizes them to realistically simulate asset price behavior.

Geometric Brownian Motion models price evolution with this formula:

$$S_{t+1} = S_t \cdot \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t} \cdot Z_t\right)$$

Where:
- $S_t$ = current price of equity
- $\mu$ = expected return
- $\sigma$ = volatility
- $\Delta t$ = time step
- $Z_t$ = random shock from a normal distribution

#### Geometric Brownian Motion used in this Project

In the context of this project, Geometric Brownian Motion is applied at each time step for every equity in the portfolio to simulate what the price would be the next day. The current price of the equity is utilized as the starting point from which the model then applies the GBM formula 252 times, once per trading day, to generate a price path for each equity with a one year time horizon. The individual paths are then aggregated based on position size in the portfolio to create the path of the portfolio value. This process is repeated for each Monte Carlo simulation to produce thousands of possible price paths for the portfolio, capturing a range of possible outcomes.

### Expected Return using Capital Asset Pricing Model (CAPM)

