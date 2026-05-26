# GBM Portfolio Simulator

Monte Carlo portfolio simulator using Geometric Brownian Motion with correlated random shocks and live market data.

---

## Project Synopsis

This program simulates potential future values of an equity portfolio using Geometric Brownian Motion and Monte Carlo simulation. Live market data is pulled from Yahoo Finance via the yfinance library and used to compute expected returns, historical volatility, and correlations between asset pairs. The simulation generates 10,000 price paths for the portfolio and outputs a graphical display of the data along with relevant metrics including VaR, Sharpe ratio, Sortino ratio, and probability of loss.

---

## Technical Approach

### Monte Carlo Simulation

#### What is Monte Carlo Simulation?

Monte Carlo simulation is a way to model the probability of different outcomes for a process whose outcome cannot be easily predicted due to the inclusion of random variables. Monte Carlo simulation is used to understand the impact of risk and uncertainty and in investing can be used to model the range of future prices of an asset. 

#### Monte Carlo Simulation Used in This Project

In this project, Monte Carlo simulation is being used to estimate thousands of possible future values of an equity portfolio. The underlying process modeled in this program is Geometric Brownian Motion. Utilizing a Monte Carlo simulation allows investors to better grasp the range of possible outcomes and their relative likelihood. This also allows for the estimation of the probability of loss, and quantifying downside risk via metrics like Value at Risk.

### Geometric Brownian Motion

#### What is Geometric Brownian Motion?

Geometric Brownian Motion (GBM) is a stochastic process used to model the evolution of an asset's price. The process originated from Brownian Motion, a concept from physics that was observed through the random movement of pollen particles in water. The "Geometric" extension came later to modify the process for the modeling of asset prices, ensuring they stay positive and grow multiplicatively. GBM assumes that asset prices follow a log-normal distribution, and therefore logarithmic returns are normally distributed. GBM is the foundation of many financial models including Black-Scholes option pricing.

#### Geometric Brownian Motion as a Concept

Geometric Brownian Motion is best understood through analogy. Consider a leaf floating down a river. Its movement is determined by two forces, the current of the river which pushes the leaf in a general direction (drift), and the deviations caused by branches, rocks, other objects in the water, and wind (random shocks). The prices of equities behave in the same manner. Expected return acts as the drift, providing a constant directional pull, while market randomness introduces volatility at each time step. GBM captures these two forces and uses them to realistically simulate asset price behavior.

Geometric Brownian Motion models price evolution with this formula:

$$S_{t+1} = S_t \cdot \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t} \cdot Z_t\right)$$

Where:
- $S_t$ = current price of equity
- $\mu$ = expected return
- $\sigma$ = volatility
- $\Delta t$ = time step
- $Z_t$ = random shock from a normal distribution

#### Geometric Brownian Motion Used in This Project

Here, Geometric Brownian Motion is applied at each time step for every equity in the portfolio to simulate what the price would be the next day. The current price of the equity is the starting point from which the model then applies the GBM formula 252 times, once per trading day, to generate a price path for each equity with a one year time horizon. The individual paths are then aggregated based on position size in the portfolio to create the path of the portfolio value. This process is repeated for each Monte Carlo simulation to produce thousands of possible price paths for the portfolio, capturing a range of possible outcomes.

### Expected Return Using the Capital Asset Pricing Model (CAPM)

#### What is the Capital Asset Pricing Model?

The Capital Asset Pricing Model (CAPM) is a financial model used to estimate the expected return of an investment based on its riskiness relative to the overall market. This is done by measuring the asset's systematic risk. Systematic risk is the market risk that cannot be diversified away, quantified by the asset's beta coefficient. 

CAPM estimates expected return with this formula:

$$\mu = R_f + \beta \cdot (R_m - R_f)$$

Where:
- $\mu$ = Expected return of the investment
- $R_f$ = Risk free rate
- $\beta$ = Beta
- $R_m$ = Expected return of the market
- $(R_m - R_f)$ = Equity Risk Premium

#### CAPM Used in This Project

In the context of this project, CAPM is used to determine the expected return for each equity within the portfolio. These expected returns serve as the drift factor inputs for the GBM calculation to determine the price of the equities at the next time step. For the risk free rate, the current yield of the 10 year treasury note (^TNX) is used. To determine the expected return of the market, the 10 year compound annual growth rate (CAGR) is used. Due to the 10 year CAGR not being adjusted for inflation, all growth estimates are nominal and not real returns.

### Historical Volatility Using Log Returns

#### Why Use Log Returns?

Volatility is measured as the standard deviation of daily returns, which is then annualized. Instead of simple daily returns, this project utilizes log returns for two reasons: 

- The issues created by the multiplicative nature of equity returns
- The asymmetric and skewed nature of simple returns

Equity returns are inherently multiplicative because they compound over time. For example, if a stock gains 10% on day one and falls 10% on day two, the equity does not return to its initial price from day zero. Taking the natural log of these returns converts them from being multiplicative to additive. This means the log return of day one plus the log return of day two gives the log return for the two day period and makes calculations cleaner. 

Simple returns are asymmetric and skewed in nature due to stock prices being unable to fall below zero, capping losses at -100%, although gains can be theoretically infinite. Transforming the returns logarithmically eliminates the skew and maps the returns symmetrically so the data fits a normal distribution.

#### Volatility Used in This Project

Here, volatility serves as the magnitude of the random shocks when determining the price of the equity at the next time step. To compute this, daily historical closing prices over the last year are taken and the daily log returns are calculated. The standard deviation of those returns is then taken and annualized to determine the volatility of the equity.

### Correlated Random Shocks

#### Why is Correlating Random Shocks Necessary?

When simulating a multi-asset portfolio, the relationships between assets needs to be accounted for. For example, AAPL and NVDA are more likely to move together than AAPL and XOM. Ignoring correlations between equities, consequently treating their random shocks as independant, improperly estimates price paths and creates illusions of diversification when not present in the portfolio. Adding equity correlations to the random shocks used in GBM takes 3 main steps:

- Calculating the correlations between asset pairs
- Converting correlation matrix to covariance matrix
- Applying Cholesky decomposition to generate correlated random shocks

Correlation is the measure of the degree to which two assets move in relation to one another. The correlation matrix is created by computing daily log returns for each equity and calculating the correlation coefficient of each asset pair. These correlation values can range from -1.0 (inversely correlated) to 1.0 (positively correlated).

The covariance matrix is then generated by capturing how much two assets move together by accounting for their individual volatilies and their correlation. An equity with high volatility that is highly correlated to another equity will have a large covariance with that equity, whereas uncorrelated equities will have a covariance near zero. The covariance matrix is simply the correlation matrix scaled by the volatilities of each asset pair.

The final step then uses Cholesky decomposition which takes the covariance matrix and produces a lower triangular matrix of weights. These weights are then applied to an array of independent random shocks through matrix multiplication. Assets with high covariance end up with shocks that tend to move in the same direction as the equities they are correlated with, while assets that have low covariance are assigned shocks that are largely independent from the others. Through this process an array of correlated random shocks is generated that mirrors how the assets in the portfolio move together.

### Graphical Output and Metrics

Upon execution, the program generates a two-part breakdown of the simulation results:

- A visual display detailing portfolio price paths and distribution of final portfolio values
- A summary of relevant portfolio metrics displayed in the console


