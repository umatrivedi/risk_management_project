import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm

class FinancialInstrument:
    """
    A base class representing a financial instrument.

    Attributes:
        ticker (str): The ticker symbol of the financial instrument.
        quantity (int or float): The quantity of the financial instrument held in the portfolio.
        data (pd.Series): Time series data for the financial instrument, typically the adjusted closing prices.
        returns (pd.Series): Daily returns of the financial instrument, computed from the data.
    """

    def __init__(self, ticker, quantity):
        """
        Initializes a financial instrument with a ticker and quantity.

        Args:
            ticker (str): The ticker symbol of the financial instrument.
            quantity (int or float): The quantity of the financial instrument held.
        """
        self.ticker = ticker
        self.quantity = quantity
        self.data = None
        self.returns = None

    def fetch_data(self, start_date, end_date):
        """
        Fetches historical data for the financial instrument within the given date range.
        Must be implemented by subclasses.

        Args:
            start_date (str): The start date for fetching data.
            end_date (str): The end date for fetching data.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses should implement this!")

    def update_quantity(self, additional_quantity):
        """
        Updates the quantity of the financial instrument by adding to the current quantity.

        Args:
            additional_quantity (int or float): The quantity to add to the current quantity.
        """
        self.quantity += additional_quantity

    def compute_returns(self):
        """
        Computes the daily returns of the financial instrument based on its historical data.
        Returns are computed as the percentage change in adjusted closing prices.
        """
        if self.data is not None:
            self.returns = self.data.pct_change().dropna()
        else:
            self.returns = pd.Series(dtype='float64')

    def get_data(self):
        """
        Accessor method to get the historical data of the financial instrument.

        Returns:
            pd.Series: The time series data of the financial instrument.
        """
        return self.data

    def get_returns(self):
        """
        Accessor method to get the daily returns of the financial instrument.

        Returns:
            pd.Series: The daily returns of the financial instrument.
        """
        return self.returns


class Stock(FinancialInstrument):
    """
    A class representing a stock, inherited from FinancialInstrument.
    """

    def fetch_data(self, start_date, end_date):
        """
        Fetches historical adjusted closing prices for the stock within the given date range.

        Args:
            start_date (str): The start date for fetching data.
            end_date (str): The end date for fetching data.

        Returns:
            pd.Series: The adjusted closing prices of the stock.

        Raises:
            Exception: If an error occurs while fetching the data.
        """
        try:
            self.data = yf.download(self.ticker, start=start_date, end=end_date)['Adj Close']
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            self.data = pd.Series(dtype='float64')
        return self.data


class Bond(FinancialInstrument):
    """
    A class representing a bond, inherited from FinancialInstrument.
    """

    def fetch_data(self, start_date, end_date):
        """
        Placeholder method for fetching historical data for the bond within the given date range.
        """
        pass


class Swap(FinancialInstrument):
    """
    A class representing a swap, inherited from FinancialInstrument.
    """

    def fetch_data(self, start_date, end_date):
        """
        Placeholder method for fetching historical data for the swap within the given date range.
        """
        pass


class Portfolio:
    """
    A class representing a portfolio of financial instruments.

    Attributes:
        instruments (dict): A dictionary of financial instruments in the portfolio, keyed by their ticker.
        returns (pd.DataFrame): A DataFrame of daily returns for each financial instrument in the portfolio.
        history (pd.Series): A time series of the portfolio's total value over time.
    """

    def __init__(self):
        """
        Initializes an empty portfolio.
        """
        self.instruments = {}
        self.returns = None
        self.history = pd.Series(dtype='float64')

    def add_instrument(self, instrument):
        """
        Adds a financial instrument to the portfolio. If the instrument is already in the portfolio,
        its quantity is updated.

        Args:
            instrument (FinancialInstrument): The financial instrument to add to the portfolio.
        """
        if instrument.ticker in self.instruments:
            self.instruments[instrument.ticker].update_quantity(instrument.quantity)
        else:
            self.instruments[instrument.ticker] = instrument

    def fetch_all_data(self, start_date, end_date):
        """
        Fetches historical data for all financial instruments in the portfolio.

        Args:
            start_date (str): The start date for fetching data.
            end_date (str): The end date for fetching data.
        """
        for instrument in self.instruments.values():
            instrument.fetch_data(start_date, end_date)

    def compute_portfolio_value(self):
        """
        Computes the portfolio's total value over time by summing the values of all financial instruments.

        Returns:
            pd.Series: A time series of the portfolio's total value.
        """
        values = []
        for instrument in self.instruments.values():
            if instrument.data is not None:
                values.append(instrument.data * instrument.quantity)
        if values:
            self.history = pd.concat(values, axis=1).sum(axis=1)
        else:
            self.history = pd.Series(dtype='float64')
        return self.history

    def compute_returns(self):
        """
        Computes the daily returns for the entire portfolio by combining the returns of all financial instruments.
        """
        returns_dict = {}
        for instrument in self.instruments.values():
            instrument.compute_returns()
            returns_dict[instrument.ticker] = instrument.returns
        if returns_dict:
            self.returns = pd.concat(returns_dict, axis=1)
        else:
            self.returns = pd.DataFrame(dtype='float64')

    def get_returns(self):
        """
        Accessor method to get the portfolio's daily returns.

        Returns:
            pd.DataFrame: The daily returns of the portfolio.
        """
        return self.returns

    def get_history(self):
        """
        Accessor method to get the portfolio's total value over time.

        Returns:
            pd.Series: The time series of the portfolio's total value.
        """
        return self.history

    def historical_var(self, time_horizon=1, percentile=0.95):
        """
        Calculates the portfolio's Value at Risk (VaR) using the historical method.

        Args:
            time_horizon (int): The time horizon over which to calculate the VaR, in days.
            percentile (float): The confidence level for the VaR calculation.

        Returns:
            float: The calculated Value at Risk (VaR) for the portfolio.

        Raises:
            ValueError: If data has not been fetched or if the portfolio is empty.
        """
        self.compute_portfolio_value()
        self.compute_returns()

        if self.returns is None or self.history.empty:
            raise ValueError("Data has not been fetched or portfolio is empty.")

        var_dict = {}
        loss_percentile = (1 - percentile) * 100

        for instrument in self.instruments.values():
            if instrument.returns.empty:
                raise ValueError(f"Return data is empty for instrument: {instrument.ticker}")

            percentile_return = np.percentile(instrument.returns, loss_percentile)
            projected_value = instrument.data.iloc[-1] * (1 + percentile_return) * instrument.quantity
            current_value = instrument.data.iloc[-1] * instrument.quantity
            var_1day = current_value - projected_value
            var_n_days = var_1day * np.sqrt(time_horizon)
            var_dict[instrument.ticker] = var_n_days

        portfolio_var = sum(var_dict.values())
        return portfolio_var

    def model_building_var(self, confidence_level=0.95, time_horizon=1):
        """
        Calculates the portfolio's Value at Risk (VaR) using the model-building (variance-covariance) method.

        Args:
            confidence_level (float): The confidence level for the VaR calculation.
            time_horizon (int): The time horizon over which to calculate the VaR, in days.

        Returns:
            float: The calculated Value at Risk (VaR) for the portfolio.

        Raises:
            ValueError: If data has not been fetched, if the portfolio is empty, or if the portfolio value is zero.
        """
        self.compute_returns()

        if self.returns is None or self.history.empty:
            raise ValueError("Data has not been fetched or portfolio is empty.")

        covariance_matrix = self.returns.cov()
        portfolio_value = self.compute_portfolio_value().iloc[-1]

        if portfolio_value == 0:
            raise ValueError("Portfolio value is zero. Cannot calculate VaR.")

        weights = np.array([instrument.data.iloc[-1] * instrument.quantity / portfolio_value for instrument in self.instruments.values()])
        portfolio_variance = np.dot(weights.T, np.dot(covariance_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        z_score = norm.ppf(1 - confidence_level)
        var_value = z_score * portfolio_volatility * portfolio_value
        var_value *= np.sqrt(time_horizon)
        return abs(var_value)

    def monte_carlo_var(self, num_simulations, time_horizon, percentile):
        """
        Calculates the portfolio's Value at Risk (VaR) using the Monte Carlo simulation method.

        Args:
            num_simulations (int): The number of Monte Carlo simulations to run.
            time_horizon (int): The time horizon over which to calculate the VaR, in days.
            percentile (float): The confidence level for the VaR calculation.

        Returns:
            float: The calculated Value at Risk (VaR) for the portfolio.

        Raises:
            ValueError: If data has not been fetched or if the portfolio is empty.
        """
        self.compute_returns()
        current_value = self.compute_portfolio_value().iloc[-1]

        if self.returns is None or self.history.empty:
            raise ValueError("Data has not been fetched or portfolio is empty.")

        weights = np.array([instrument.data.iloc[-1] * instrument.quantity / current_value for instrument in self.instruments.values()])
        mean_returns = self.returns.mean()
        covariance_matrix = self.returns.cov()
        simulated_returns = np.random.multivariate_normal(mean_returns, covariance_matrix, num_simulations)
        simulated_portfolio_returns = np.dot(simulated_returns, weights)
        portfolio_percent_changes = simulated_portfolio_returns * np.sqrt(time_horizon)
        var_percentile = np.percentile(portfolio_percent_changes, 100 - (percentile * 100))
        var_projected_value = current_value * (1 + var_percentile)
        var_loss = current_value - var_projected_value
        return var_loss
