import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend import *

class PortfolioApp:
    """
    A class to create a graphical user interface (GUI) application for managing a portfolio 
    and calculating Value at Risk (VaR) using different methodologies.
    
    Attributes:
        root (tk.Tk): The main Tkinter window.
        portfolio (Portfolio): The portfolio object containing the financial instruments.
        start_date (str): The start date for data fetching.
        end_date (str): The end date for data fetching.
    """
    def __init__(self, root, portfolio):
        """
        Initializes the PortfolioApp with a root window and a portfolio object.
        
        Args:
            root (tk.Tk): The main Tkinter window.
            portfolio (Portfolio): The portfolio object containing financial instruments.
        """
        self.root = root
        self.root.title("Portfolio VaR Calculator")
        self.root.geometry("600x500")
        
        self.portfolio = portfolio
        self.start_date = None
        self.end_date = None
        
        # Title Label
        self.title_label = tk.Label(root, text="Portfolio Value at Risk (VaR) Calculator", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Add Stock Button
        self.add_stock_button = tk.Button(root, text="Add Stock", command=self.open_add_stock_window)
        self.add_stock_button.pack(pady=5)

        # Select Timeframe Button
        self.select_timeframe_button = tk.Button(root, text="Select Timeframe", command=self.open_timeframe_window)
        self.select_timeframe_button.pack(pady=5)

        # Fetch Data Button
        self.fetch_data_button = tk.Button(root, text="Fetch Data", command=self.fetch_data)
        self.fetch_data_button.pack(pady=5)

        # Plot Portfolio Data Button
        self.plot_portfolio_data_button = tk.Button(root, text="Plot Portfolio Data", command=self.plot_portfolio_data)
        self.plot_portfolio_data_button.pack(pady=5)

        # Plot Stock Data Button
        self.plot_stock_data_button = tk.Button(root, text="Plot Stock Data", command=self.plot_stock_data)
        self.plot_stock_data_button.pack(pady=5)

        # View Portfolio Button
        self.view_portfolio_button = tk.Button(root, text="View Portfolio", command=self.open_view_portfolio_window)
        self.view_portfolio_button.pack(pady=5)

        # Historical VaR Button
        self.historical_var_button = tk.Button(root, text="Calculate Historical VaR", command=self.open_historical_var_window)
        self.historical_var_button.pack(pady=5)

        # Monte Carlo VaR Button
        self.monte_carlo_var_button = tk.Button(root, text="Calculate Monte Carlo VaR", command=self.open_monte_carlo_var_window)
        self.monte_carlo_var_button.pack(pady=5)

        # Parametric VaR Button
        self.parametric_var_button = tk.Button(root, text="Calculate Parametric VaR", command=self.open_parametric_var_window)
        self.parametric_var_button.pack(pady=5)

    def open_add_stock_window(self):
        """
        Opens a new window to allow the user to add a stock to the portfolio.
        """
        add_stock_window = tk.Toplevel(self.root)
        add_stock_window.title("Add Stock")

        tk.Label(add_stock_window, text="Ticker:").grid(row=0, column=0, padx=10, pady=10)
        self.ticker_entry = tk.Entry(add_stock_window)
        self.ticker_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_stock_window, text="Quantity:").grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(add_stock_window)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        add_button = tk.Button(add_stock_window, text="Add", command=self.add_stock)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

    def open_timeframe_window(self):
        """
        Opens a new window to allow the user to select the timeframe for data fetching.
        """
        timeframe_window = tk.Toplevel(self.root)
        timeframe_window.title("Select Timeframe")

        tk.Label(timeframe_window, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.start_date_entry = tk.Entry(timeframe_window)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(timeframe_window, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        self.end_date_entry = tk.Entry(timeframe_window)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=10)

        confirm_button = tk.Button(timeframe_window, text="Confirm", command=self.set_timeframe)
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

    def set_timeframe(self):
        """
        Sets the start and end dates for data fetching based on user input.
        """
        self.start_date = self.start_date_entry.get()
        self.end_date = self.end_date_entry.get()
        messagebox.showinfo("Timeframe Set", f"Start Date: {self.start_date}\nEnd Date: {self.end_date}")

    def fetch_data(self):
        """
        Fetches data for the portfolio based on the selected timeframe and calculates 
        the portfolio value and returns. Displays a message on success or error.
        """
        if self.start_date and self.end_date:
            self.portfolio.fetch_all_data(self.start_date, self.end_date)
            self.portfolio.compute_portfolio_value()
            self.portfolio.compute_returns()
            messagebox.showinfo("Info", "Data fetched successfully.")
        else:
            messagebox.showerror("Error", "Please select a timeframe first.")

    def plot_portfolio_data(self):
        """
        Plots the portfolio value over time if data has been fetched and the portfolio is not empty.
        """
        if self.portfolio.history.empty:
            messagebox.showerror("Error", "No data has been fetched or portfolio is empty.")
        else:
            plt.figure()
            plt.plot(self.portfolio.history.index, self.portfolio.history.values)
            plt.title("Portfolio Value Over Time")
            plt.xlabel("Date")
            plt.ylabel("Portfolio Value")
            plt.show()

    def plot_stock_data(self):
        """
        Plots the stock prices over time for all stocks in the portfolio if the portfolio is not empty.
        """
        if not self.portfolio.instruments:
            messagebox.showerror("Error", "No stocks in portfolio.")
            return

        plot_window = tk.Toplevel(self.root)
        plot_window.title("Stock Data Plot")

        fig, ax = plt.subplots()

        for instrument in self.portfolio.instruments.values():
            ax.plot(instrument.get_data().index, instrument.get_data().values, label=instrument.ticker)

        ax.set_title("Stock Prices Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Stock Price")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def add_stock(self):
        """
        Adds a stock to the portfolio based on user input for ticker and quantity.
        Displays a message on success or error.
        """
        ticker = self.ticker_entry.get().upper()
        quantity = int(self.quantity_entry.get())

        if ticker and quantity > 0:
            stock = Stock(ticker, quantity)
            self.portfolio.add_instrument(stock)
            messagebox.showinfo("Success", f"Added {quantity} of {ticker} to the portfolio.")
        else:
            messagebox.showerror("Error", "Please enter valid ticker and quantity.")

    def open_view_portfolio_window(self):
        """
        Opens a new window to display the current portfolio, listing each stock's ticker and quantity.
        """
        view_portfolio_window = tk.Toplevel(self.root)
        view_portfolio_window.title("Portfolio")

        tree = ttk.Treeview(view_portfolio_window, columns=("Ticker", "Quantity"), show="headings")
        tree.heading("Ticker", text="Ticker")
        tree.heading("Quantity", text="Quantity")
        tree.pack(fill="both", expand=True)

        for ticker, instrument in self.portfolio.instruments.items():
            tree.insert("", "end", values=(ticker, instrument.quantity))

    def open_historical_var_window(self):
        """
        Opens a new window to calculate Historical VaR based on user input for 
        confidence level and time horizon.
        """
        var_window = tk.Toplevel(self.root)
        var_window.title("Calculate Historical VaR")

        tk.Label(var_window, text="Confidence Level (0-1):").grid(row=0, column=0, padx=10, pady=10)
        self.confidence_level_entry = tk.Entry(var_window)
        self.confidence_level_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(var_window, text="Time Horizon (days):").grid(row=1, column=0, padx=10, pady=10)
        self.time_horizon_entry = tk.Entry(var_window)
        self.time_horizon_entry.grid(row=1, column=1, padx=10, pady=10)

        calculate_button = tk.Button(var_window, text="Calculate", command=self.calculate_historical_var)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    def open_monte_carlo_var_window(self):
        """
        Opens a new window to calculate Monte Carlo VaR based on user input for 
        confidence level, time horizon, and number of simulations.
        """
        var_window = tk.Toplevel(self.root)
        var_window.title("Calculate Monte Carlo VaR")

        tk.Label(var_window, text="Confidence Level (0-1):").grid(row=0, column=0, padx=10, pady=10)
        self.confidence_level_entry = tk.Entry(var_window)
        self.confidence_level_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(var_window, text="Time Horizon (days):").grid(row=1, column=0, padx=10, pady=10)
        self.time_horizon_entry = tk.Entry(var_window)
        self.time_horizon_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(var_window, text="Number of Simulations:").grid(row=2, column=0, padx=10, pady=10)
        self.num_simulations_entry = tk.Entry(var_window)
        self.num_simulations_entry.grid(row=2, column=1, padx=10, pady=10)

        calculate_button = tk.Button(var_window, text="Calculate", command=self.calculate_monte_carlo_var)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

    def open_parametric_var_window(self):
        """
        Opens a new window to calculate Parametric (Model Building) VaR based on user input for 
        confidence level and time horizon.
        """
        var_window = tk.Toplevel(self.root)
        var_window.title("Calculate Parametric VaR")

        tk.Label(var_window, text="Confidence Level (0-1):").grid(row=0, column=0, padx=10, pady=10)
        self.confidence_level_entry = tk.Entry(var_window)
        self.confidence_level_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(var_window, text="Time Horizon (days):").grid(row=1, column=0, padx=10, pady=10)
        self.time_horizon_entry = tk.Entry(var_window)
        self.time_horizon_entry.grid(row=1, column=1, padx=10, pady=10)

        calculate_button = tk.Button(var_window, text="Calculate", command=self.calculate_parametric_var)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_historical_var(self):
        """
        Calculates Historical VaR based on the user-provided confidence level and time horizon. 
        Displays the calculated VaR in a message box.
        """
        confidence_level = float(self.confidence_level_entry.get())
        time_horizon = int(self.time_horizon_entry.get())

        var = self.portfolio.historical_var(confidence_level, time_horizon)
        messagebox.showinfo("Historical VaR", f"VaR: {var}")

    def calculate_monte_carlo_var(self):
        """
        Calculates Monte Carlo VaR based on the user-provided confidence level, time horizon, 
        and number of simulations. Displays the calculated VaR in a message box.
        """
        confidence_level = float(self.confidence_level_entry.get())
        time_horizon = int(self.time_horizon_entry.get())
        num_simulations = int(self.num_simulations_entry.get())

        var = self.portfolio.monte_carlo_var(confidence_level, time_horizon, num_simulations)
        messagebox.showinfo("Monte Carlo VaR", f"VaR: {var}")

    def calculate_parametric_var(self):
        """
        Calculates Parametric (Model Building) VaR based on the user-provided confidence level 
        and time horizon. Displays the calculated VaR in a message box.
        """
        confidence_level = float(self.confidence_level_entry.get())
        time_horizon = int(self.time_horizon_entry.get())

        var = self.portfolio.parametric_var(confidence_level, time_horizon)
        messagebox.showinfo("Parametric VaR", f"VaR: {var}")

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    portfolio = Portfolio()  # Assuming Portfolio is a class you've defined in backend.py
    app = PortfolioApp(root, portfolio)
    root.mainloop()
