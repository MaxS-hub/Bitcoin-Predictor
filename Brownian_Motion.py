import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt

#Probably will change this
from Database import start, end, prediction_days
model = 'Brownian Motion'

#Import current Bitcoin price

s = start.strftime("%Y-%m-%d")
e = end.strftime("%Y-%m-%d")

P = web.get_data_tiingo('btcusd',s,e, api_key = ('eef2cf8be7666328395f2702b5712e533ea072b9'))
P = P['close'].values
val = np.float64(P[-1])
a = val.item()


#Create Brownian Motion
class Brownian():
    
    """
    A Brownian motion class constructor
    """

    def __init__(self, x0=0,s0=100):
        """
        Init class
        """
        assert (type(x0) == float or type(x0) == int or x0 is None), "Expect a float or None for the initial value"
        assert (type(s0) == float or type(s0) == int or s0 is None or s0 != 0), \
            "Expect a float or None for the initial stock price and has to be > 0"

        self.x0 = float(x0)

        self.s0 = float(s0)

    def gen_random_walk(self, n_step=100):
        """
        Generate motion by random walk

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        # Warning about the small number of steps
        if n_step < 30:
            print("WARNING! The number of steps is small. It may not generate a good stochastic process sequence!")

        w = np.ones(n_step) * self.x0

        for i in range(1, n_step):
            # Sampling from the Normal distribution with probability 1/2
            yi = np.random.choice([1, -1])
            # Weiner process
            w[i] = w[i - 1] + (yi / np.sqrt(n_step))

        return w

    def gen_normal(self, n_step=100, sigma = 1):
        """
        Generate motion by drawing from the Normal distribution

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        if n_step < 30:
            print("WARNING! The number of steps is small. It may not generate a good stochastic process sequence!")

        w = np.ones(n_step) * self.x0

        for i in range(1, n_step):
            # Sampling from the Normal distribution
            yi = np.random.normal(scale = sigma)
            # Weiner process
            w[i] = w[i - 1] + (yi / np.sqrt(n_step))

        return w

    def stock_price(self,mu=0.25,sigma=0.68,deltaT=60,dt=1):
        """
        Models a stock price S(t) using the Weiner process W(t) as
        `S(t) = S(0).exp{(mu-(sigma^2/2).t)+sigma.W(t)}`

        Arguments:
            s0: Initial stock price, default 100
            mu: 'Drift' of the stock (upwards or downwards), default 0.2
            sigma: 'Volatility' of the stock, default 0.68
            deltaT: The time period for which the future prices are computed, default 52 (as in 52 weeks)
            dt (optional): The granularity of the time-period, default 0.1

        Returns:
            s: A NumPy array with the simulated stock prices over the time-period deltaT
        """
        n_step = int(deltaT / dt)
        time_vector = np.linspace(0, deltaT, num=n_step)
        # Stock variation
        stock_var = (mu - ((sigma ** 2) / 2)) * time_vector
        # Forcefully set the initial value to zero for the stock price simulation
        self.x0 = 0
        # Weiner process (calls the `gen_normal` method)
        weiner_process = sigma * self.gen_normal(n_step)
        # Add two time series, take exponent, and multiply by the initial stock price
        s = self.s0 * (np.exp(stock_var + weiner_process))

        return s


b = Brownian(s0=a)

results = b.stock_price(deltaT = prediction_days)
np.savetxt('data/results',results)
#With historical mu and sigma for Bitcoin:
'''
mu = 2556.866219
sigma = 3606.743821
res = b.stock_price(mu=2557, sigma=3607)
'''
