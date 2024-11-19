# Option Pricing Tool
## Very basic option pricing tool for call and put options.

* The goal of this project is to compute the price of call and put options for given inputs.
* The tool also gives other information, about greeks for now. I would like to add nice visuals.

* All greeks are computed with numerical derivatives:
    for example vega (dC/dsigma):
    1. compute price
    2. nudge sigma
    3. compute price
    4. compute derivative
    
## BS Forumla:

C = S * N(d1) - K * e^(-r * t) * N(d2) \

d1 = ( ln(S0 / K) + (r + sigma^2 / 2) * T ) / sigma * sqrt(T) \
d2 = ( ln(S0 / K) + (r - sigma^2 / 2) * T ) / sigma * sqrt(T) \


C = Call option price \
S = current stock price \
K = strike price \
r = risk-free interest rate \
t = time to maturity \
N = Normal distribution (cumulative)
