from typing import Tuple
import numpy as np
from scipy.stats import norm

e = 1e-6

class BlackScholes:
    """
    A class to calculate option prices using the Black-Scholes model.
    """
    
    def __init__(
        self,
        price_u_0: float,
        strike_price : float,
        time_to_maturity : float,
        risk_free : float,
        sigma : float,
        option_type : str = "call"
    ):
        """
        Initialize Black-Scholes calculator with option parameters.
        
        Args:
            price_u_0 (float): Current option_price of the underlying asset
            stike_price (float): Strike option_price of the option
            time_to_maturity (float): Time to expiration in years
            risk_free (float): Risk-free interest rate (decimal)
            sigma (float): Implied volatility of the underlying asset (decimal)
        """
            
        self.price_u_0 = price_u_0 
        self.strike_price = strike_price 
        self.time_to_maturity = time_to_maturity # 1 is 1 year
        self.risk_free_rate = risk_free
        self.sigma = sigma # in % terms
        self.option_type = option_type
        
    def _calculate_d1_d2(self) -> Tuple[float, float]:
        """Calculate d1 and d2 parameters for the Black-Scholes formula."""
        d1 = d1 = ( np.log( self.price_u_0 / self.strike_price ) + (self.risk_free_rate + self.sigma**2 / 2) * self.time_to_maturity ) / self.sigma * np.sqrt(self.time_to_maturity)
        d2 = d1 - self.sigma * np.sqrt(self.time_to_maturity)
        return d1, d2
        
    def calculate_price(self) -> float:
        """
        Calculate the option option_price according to the Black-Scholes-Merton formula.
        
        Args:
            option_type (str): Type of option ('call' or 'put')
            
        Returns:
            float: Calculated option option_price
        """

        if self.option_type not in ['call', 'put']:
            raise ValueError("Option type must be either 'call' or 'put'")
            
        d1, d2 = self._calculate_d1_d2()
        
        if self.option_type == 'call':
            option_price = self.price_u_0 * norm.cdf(d1) - self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(d2)
        else:  # put
            option_price = self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(-d2) - self.price_u_0 * norm.cdf(-d1)
            
        return option_price
        
    def get_delta(self):

        # delta:
        # sensitivity to option_price of underlying 
        
        option_price = self.calculate_price()

        original_price = self.price_u_0
        self.price_u_0 += e # small increment in price of underlying to compute numerical derivative
        option_price_increment_u = self.calculate_price() # compute value of option after small increment in the value of the underlying
        self.price_u_0 = original_price # reset price of the underlying to the original value


        delta = (option_price_increment_u - option_price) / e

        return delta
    
    def get_gamma(self):

        # compute gamma of option. How delta changes when the price of the underlying changes

        option_delta = self.get_delta()
        original_price = self.price_u_0
        self.price_u_0 += e
        option_delta_increment_u = self.get_delta()
        self.price_u_0 = original_price

        gamma = ( option_delta_increment_u - option_delta ) / e

        return gamma
    
    def get_vega(self):

        # compute vega of option. How value of the option changes when the volatility of the underlying changes

        option_price = self.calculate_price() # price of option at original volatility
        original_sigma = self.sigma
        self.sigma += e # nudge in volatility
        option_price_increment_sigma = self.calculate_price() # price after the nudge
        self.sigma = original_sigma

        vega = ( option_price_increment_sigma - option_price ) / e # derivative w.r.t. sigma (volatility)

        return vega
    
    def get_theta(self):
        
        # Calculate option price at the current time to maturity
        price_at_t = self.calculate_price()
        original_time_to_maturity = self.time_to_maturity

        # Decrease time to maturity slightly (simulate passage of time)
        self.time_to_maturity -= e
        price_at_t_minus_epsilon = self.calculate_price()

        # Restore original time to maturity
        self.time_to_maturity = original_time_to_maturity

        # Compute theta (negative because it's typically a cost over time)
        theta = (price_at_t_minus_epsilon - price_at_t) / e

        return theta
    
    def get_rho(self):

        original_risk_free = self.risk_free_rate
        price_at_r = self.calculate_price()

        self.risk_free_rate += e

        price_at_r_nudged = self.calculate_price()
        self.risk_free_rate = original_risk_free

        rho = (price_at_r_nudged - price_at_r ) / e

        return rho
        
    


