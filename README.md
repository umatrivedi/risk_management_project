Portfolio Value at Risk Calculator

# Overview

This Python project implements a Portfolio Value at Risk Calculator that handles different financial instruments (stocks for now- implementation for bonds and swaps requires paid data) and performs risk analysis using various Value at Risk (VaR) methodologies. The system is designed to fetch financial data, compute portfolio values, plot data, and calculate VaR using Historical, Model-Building (Parametric), and Monte Carlo simulation methods.

# Prerequisites

Python 3.x
Required Python libraries:
yfinance
numpy
pandas
scipy

You can install the required libraries using pip:

```python
pip install yfinance numpy pandas scipy

```
# Installation

Clone this repository to your local machine:

```python
git clone https://github.com/umatrivedi/risk_management_project.git
cd portfolio-risk-management
```

# Usage

**Using the Graphical User Interface 
**

Launch the Application:
Run the portfolio_var_calculator.py script to open the GUI application.

Add Stocks:
Click the "Add Stock" button to open a window where you can enter the ticker symbol and quantity of the stock.
Click "Add" to add the stock to your portfolio.

Select Timeframe:
Click the "Select Timeframe" button to open a window where you can enter the start and end dates for data retrieval.
Click "Confirm" to set the timeframe.

Fetch Data:
Click the "Fetch Data" button to download historical price data for all stocks in your portfolio based on the selected timeframe.

View Portfolio:
Click the "View Portfolio" button to open a window that displays the current portfolio with tickers and quantities.

Plot Data:
Click the "Plot Portfolio Data" button to plot the portfolio value over time.
Click the "Plot Stock Data" button to open a window with a plot of each stock's price over time.

Calculate VaR:

Historical VaR:
Click "Calculate Historical VaR" to open a window where you can enter the confidence level and time horizon for historical VaR calculation.
Click "Calculate" to view the Historical VaR result.

Monte Carlo VaR:
Click "Calculate Monte Carlo VaR" to open a window where you can enter the confidence level, time horizon, and number of simulations for Monte Carlo VaR calculation.
Click "Calculate" to view the Monte Carlo VaR result.

Parametric VaR:
Click "Calculate Parametric VaR" to open a window where you can enter the confidence level and time horizon for Parametric VaR calculation.
Click "Calculate" to view the Parametric VaR result.

**If you are unable to launch the GUI use the example code below to test the calculator
**
```python
#Create instances of Stock, Bond, or Swap by specifying the ticker symbol and quantity.

from portfolio import Stock, Bond, Swap, Portfolio

stock1 = Stock('AAPL', 10)
bond1 = Bond('US10Y', 5)

#Add created instruments to your portfolio.

portfolio = Portfolio()
portfolio.add_instrument(stock1)
portfolio.add_instrument(bond1)

#Fetch historical data for all instruments in the portfolio and calculate the portfolio's total value.


portfolio.fetch_all_data('2023-01-01', '2023-12-31')
portfolio_value = portfolio.compute_portfolio_value()
print(portfolio_value)

#Calculate the Value at Risk (VaR) using different methods.

historical_var = portfolio.historical_var(time_horizon=1, percentile=0.95)
parametric_var = portfolio.model_building_var(confidence_level=0.95, time_horizon=1)
monte_carlo_var = portfolio.monte_carlo_var(num_simulations=10000, time_horizon=1, percentile=0.95)
print(f"Historical VaR: {historical_var}")
print(f"Parametric VaR: {parametric_var}")
print(f"Monte Carlo VaR: {monte_carlo_var}")

```

# Future Work
Implement data fetching for Bonds and Swaps. This requires access to Bloomberg / Reuters Data 
Extend the system to handle additional risk metrics (e.g., Expected Shortfall).
Integrate advanced pricing libraries for Bonds and Swaps.

# License
This project is licensed under the MIT License
